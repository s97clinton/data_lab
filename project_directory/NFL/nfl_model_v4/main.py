import sys
import os
current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(parent_dir)

from function_library.py_predictive_modeling.model_wrappers_sci_kit_learn import multinomial_logistic_regression
from functions.data_transformation import prep_nfl_data_py_pbp, filter_and_subset_nfl_data_py_pbp, nfl_data_py_pbp_to_drives, filter_and_subset_nfl_drive_df, nfl_data_py_weekly_transform_import, prep_schedule_data, convert_schedule_to_test_frame
from functions.feature_engineering import create_features_nfl_data_py

from datetime import datetime
import nfl_data_py as nfl
import urllib

def nfl_model_v4(future_projection: bool, training_set_seasons: list[int], test_split_season: int, test_split_week: int, import_weekly_data: bool=False):
    """
    Function:
    -Main function for NFL Model Version 4; the use_nfl_data_py_weekly parameter is set to false
    due to issues loading data that way for the 2025 season.

    Parameters:
    <seasons> (list[int]): A list of integers denoting the NFL seasons to include in training data.

    Returns:
    <pbp_df> (DataFrame): Temporary return to verify initial data load is working.
    <drive_df> (DataFrame): Temporary return to verify initial data load is working.s
    """
    pbp_import_df = nfl.import_pbp_data(years = training_set_seasons)
    schedule_import_df = nfl.import_schedules(years = training_set_seasons)
    schedule_df = prep_schedule_data(schedule_import_df)
    base_df = prep_nfl_data_py_pbp(pbp_import_df)
    pbp_df = filter_and_subset_nfl_data_py_pbp(base_df)
    pbp_df = create_features_nfl_data_py(pbp_df)
    drive_df = nfl_data_py_pbp_to_drives(base_df)
    drive_df = filter_and_subset_nfl_drive_df(drive_df)
    if import_weekly_data:
        try:
            weekly_import_df = nfl.import_weekly_data(years = training_set_seasons)
            weekly_df = nfl_data_py_weekly_transform_import(weekly_import_df)
        except urllib.error.HTTPError as e:
            print(f"The request to nfl.import_weekly_data() returned a {e}; check whether the season values passed are supported.")

    if future_projection:
        drive_train_df = drive_df
        drive_test_df = convert_schedule_to_test_frame(schedule_import_df, test_split_season, test_split_week)
        test_set_target = False
    else:        
        drive_train_df = drive_df[~((drive_df['season'] == test_split_season) & (drive_df['week'] > test_split_week))]
        drive_test_df = drive_df[((drive_df['season'] == test_split_season) & (drive_df['week'] > test_split_week))]
        test_set_target = True
    if test_set_target:
        test_output, x_test, y_pred, y_prob, pipeline, y_test, report, log_loss_score = multinomial_logistic_regression(train_set = drive_train_df, 
                                                                             test_set = drive_test_df, 
                                                                             target = ['drive_result'],
                                                                             features = ['offense','defense','home_team_on_offense'],
                                                                             one_hot_features = ['offense','defense','home_team_on_offense'],
                                                                             test_set_target=test_set_target)
    else:
        test_output, x_test, y_pred, y_prob_df = multinomial_logistic_regression(train_set = drive_train_df, 
                                                                             test_set = drive_test_df, 
                                                                             target = ['drive_result'],
                                                                             features = ['offense','defense','home_team_on_offense'],
                                                                             one_hot_features = ['offense','defense','home_team_on_offense'],
                                                                             test_set_target=test_set_target)
        
        # game_projections = pd.DataFrame() #end goal
    
    return pbp_df, drive_df, test_output


if __name__ == "__main__":
    model_start_time = datetime.now()
    pbp_df, drive_df, test_output = nfl_model_v4(future_projection=True, 
                                                 training_set_seasons=[2023, 2024, 2025], 
                                                 test_split_season=2025,
                                                 test_split_week=9,
                                                 import_weekly_data=False)
    pbp_df.to_csv("csv_output/pbp_df.csv", index=False)
    drive_df.to_csv("csv_output/drive_df.csv", index=False)
    test_output.to_csv("csv_output/test_output.csv", index=False)
    model_end_time = datetime.now()
    print(f"The model run time came in at {model_end_time - model_start_time}")
    
