from functions.import_data import *
from functions.transform_data import prep_nfl_model_data, prep_drive_test_frames
from functions.model_wrappers import multinomial_logistic_regression
from functions.model_output import drive_multinomial_results_to_drive_outcome
from datetime import datetime

write_results_db = 0
fantasy_player_projections = 0

def nfl_model_v3(start_season: int, current_season: int, projection_weeks: list[int]) -> None:
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
    pfr_game_basic, pfr_game_ids = import_pfr_game_basic(start_season, current_season)
    pfr_team_stats = import_pfr_team_stats(pfr_game_ids)
    pfr_pass_df = import_pfr_pass_df(pfr_game_ids)
    pfr_rush_df = import_pfr_rush_df(pfr_game_ids)
    pfr_rec_df = import_pfr_rec_df(pfr_game_ids)
    pfr_drive_df = import_pfr_drive_info(start_season, current_season)
    print(pfr_pass_df.head())

    for game_wk in projection_weeks:
        current_rating_df = import_current_rating(current_season, game_wk)
    #     rush_train_df, rec_train_df, drive_train_df = prep_nfl_model_data(current_rating_df, hist_rating_df, coach_qb_df, pfr_rush_df, pfr_rec_df, pfr_drive_df, current_season = current_season, current_week = game_wk)
    #     drive_test_df = prep_drive_test_frames(nfl_schedule, current_rating_df, game_wk)
        
    #     drive_test_df.to_csv("nfl_model_v3/imported_data/drive_test_df.csv")

    #     features = ['off_rating','def_rating','venue']
    #     one_hot_features = ['venue']
    #     target = ['drive_result']
    #     test_output, x_test, y_pred, y_prob_df = multinomial_logistic_regression(drive_train_df, drive_test_df, features, target, one_hot_features=one_hot_features)
    #     drive_projections = drive_multinomial_results_to_drive_outcome(test_output)
    #     print(test_output)
    #     print(drive_projections)

    nfl_schedule.to_csv("imported_data/nfl_schedule.csv")
    pfr_rush_df.to_csv("imported_data/rush_train_df.csv")
    pfr_rec_df.to_csv("imported_data/rec_train_df.csv")
    pfr_drive_df.to_csv("imported_data/drive_train_df.csv")
    # rush_train_df.to_csv("imported_data/rush_train_df.csv")
    # rec_train_df.to_csv("imported_data/rec_train_df.csv")
    # drive_train_df.to_csv("imported_data/drive_train_df.csv")

    # drive_projections.to_csv("nfl_model_v3/output_data/drive_projections.csv")

    model_end_time = datetime.now()
    print(model_end_time - model_start_time)

if __name__ == '__main__':
    nfl_model_v3(start_season = 2022, current_season = 2025, projection_weeks = list(range(8,9)))


