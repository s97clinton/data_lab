import sys
import os
current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(parent_dir)
from function_library.py_predictive_modeling.model_wrappers_sci_kit_learn import multinomial_logistic_regression
from datetime import datetime

from functions.import_data import import_schedule_csv, import_historic_rating, import_coach_qb, import_game_basic, import_team_stats, import_pass_df, import_rush_df, import_rec_df, import_drive_info, import_current_rating
from functions.transform_data import prep_nfl_model_data, prep_drive_test_frames, convert_drive_results_to_drive_points

def nfl_model_v3(start_season: int, current_season: int, projection_weeks: list[int], fantasy_player_projections: bool = False, write_results_db: bool = False) -> None:
    """
    Main function to run the NFL model version 3.
    """
    model_start_time = datetime.now()
    nfl_seasons = list(range(start_season, current_season + 1))
    nfl_weeks = list(range(1,23))
    nfl_teams = ['ARI','ATL','BAL','BUF','CAR','CHI','CIN','CLE','DAL','DEN','DET','GB','HOU','IND','JAX','KC','LAC','LAR','LVR','MIA','MIN','NE','NO','NYG','NYJ','PHI','PIT','SEA','SF','TB','TEN','WSH']

    nfl_schedule = import_schedule_csv(current_season)
    hist_rating_df = import_historic_rating(start_season, current_season)
    coach_qb_df = import_coach_qb(start_season, current_season)
    game_basic, game_ids = import_game_basic(start_season, current_season)
    team_stats = import_team_stats(game_ids)
    pass_df = import_pass_df(game_ids)
    rush_df = import_rush_df(game_ids)
    rec_df = import_rec_df(game_ids)
    drive_df = import_drive_info(start_season, current_season)
    drive_count_df = drive_df.groupby(['season','week','off','def']).size().reset_index(name='drive_count')
    drive_count_df = drive_count_df.groupby(['off','season']).agg({'drive_count':'mean'}).reset_index()
    drive_count_df.rename(columns={'drive_count':'avg_drives_per_game'}, inplace=True)

    for game_wk in projection_weeks:
        current_rating_df = import_current_rating(current_season, game_wk)
        rush_train_df, rec_train_df, drive_train_df = prep_nfl_model_data(current_rating_df, hist_rating_df, coach_qb_df, rush_df, rec_df, drive_df, current_season, game_wk)
        drive_test_df = prep_drive_test_frames(nfl_schedule, current_rating_df, game_wk)

        test_output, x_test, y_pred, y_prob_df = multinomial_logistic_regression(train_set = drive_train_df, 
                                                                                 test_set = drive_test_df, 
                                                                                 target = ['drive_result'],
                                                                                 features = ['off_rating','def_rating','venue'],
                                                                                 one_hot_features = ['venue'])
        game_projections = convert_drive_results_to_drive_points(test_output, drive_count_df, nfl_schedule, current_season, game_wk)
        game_projections.to_csv(f"result_dump/{current_season}_game_projections_week_{game_wk}.csv")
        print(game_projections)

    model_end_time = datetime.now()
    print(model_end_time - model_start_time)

if __name__ == '__main__':
    nfl_model_v3(start_season = 2022, current_season = 2025, projection_weeks = list(range(8,10)))


