from functions.import_scripts import run_nfl_data_import, import_current_rating
from functions.transform_data import prep_nfl_model_data, prep_drive_test_frames
from functions.model_wrappers import multinomial_logistic_regression
from functions.model_output import drive_multinomial_results_to_drive_outcome
from model_parameters import *

def nfl_model_v3():
    model_start_time = datetime.now()
    nfl_schedule, hist_rating_df, coach_qb_df,  pfr_game_basic, pfr_team_stats, pfr_pass_df, pfr_rush_df, pfr_rec_df, pfr_drive_df = run_nfl_data_import(start_season, current_season)

    for game_wk in projection_weeks:
        current_rating_df = import_current_rating(current_season, game_wk)
        rush_train_df, rec_train_df, drive_train_df = prep_nfl_model_data(current_rating_df, hist_rating_df, coach_qb_df, pfr_rush_df, pfr_rec_df, pfr_drive_df, current_season = current_season, current_week = game_wk)
        drive_test_df = prep_drive_test_frames(nfl_schedule, current_rating_df, game_wk)
        
        drive_test_df.to_csv("nfl_model_v3/imported_data/drive_test_df.csv")

        features = ['off_rating','def_rating','venue']
        one_hot_features = ['venue']
        target = ['drive_result']
        test_output, x_test, y_pred, y_prob_df = multinomial_logistic_regression(drive_train_df, drive_test_df, features, target, one_hot_features=one_hot_features)
        drive_projections = drive_multinomial_results_to_drive_outcome(test_output)
        print(test_output)
        print(drive_projections)

    nfl_schedule.to_csv("nfl_model_v3/imported_data/nfl_schedule.csv")
    rush_train_df.to_csv("nfl_model_v3/imported_data/rush_train_df.csv")
    rec_train_df.to_csv("nfl_model_v3/imported_data/rec_train_df.csv")
    drive_train_df.to_csv("nfl_model_v3/imported_data/drive_train_df.csv")

    drive_projections.to_csv("nfl_model_v3/output_data/drive_projections.csv")

    model_end_time = datetime.now()
    print(model_end_time - model_start_time)

if __name__ == '__main__':
    nfl_model_v3()


