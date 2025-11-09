import sys
import os
current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(parent_dir)

from functions.import_data_parquet import NFLDataLoader
from functions.import_data_csv import import_custom_ratings
from functions.data_transformation import (prep_nfl_data_py_pbp, filter_and_subset_nfl_data_py_pbp, nfl_data_py_pbp_to_drives, 
                                           filter_and_subset_nfl_drive_df, nfl_data_py_weekly_transform_import, prep_schedule_data, 
                                           convert_schedule_to_test_frame, convert_test_output_to_game_outcomes)
from functions.feature_engineering import create_features_nfl_data_py
from function_library.py_predictive_modeling.sci_kit_learn_functions import build_multinomial_log_reg_pipeline, project_multinomial_test_set, create_multinomial_metrics_report

from datetime import datetime
import nfl_data_py as nfl
import urllib

def nfl_model_v4(future_projection: bool, 
                 training_set_seasons: list[int], 
                 test_split_season: int, 
                 test_split_week: int,
                 import_weekly_data: bool=False, 
                 import_custom_rating: bool=True,
                 run_on_live_connections: bool=False):
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
    if run_on_live_connections:
        pbp_import_df = nfl.import_pbp_data(years = training_set_seasons)
        schedule_import_df = nfl.import_schedules(years = training_set_seasons)
    else:
        nfl_data_loader = NFLDataLoader()
        pbp_import_df = nfl_data_loader.pbp(seasons = training_set_seasons)
        schedule_import_df = nfl_data_loader.schedule(seasons = training_set_seasons)

    schedule_df = prep_schedule_data(schedule_import_df)
    base_df = prep_nfl_data_py_pbp(pbp_import_df)
    pbp_df = filter_and_subset_nfl_data_py_pbp(base_df)
    pbp_df = create_features_nfl_data_py(pbp_df)
    drive_df = nfl_data_py_pbp_to_drives(base_df)
    drive_df = filter_and_subset_nfl_drive_df(drive_df)
    if import_custom_rating:
        off_rating_df, def_rating_df = import_custom_ratings()
        pbp_df = pbp_df.merge(off_rating_df, how = 'left', on = ['season', 'offense'])
        pbp_df = pbp_df.merge(def_rating_df, how = 'left', on = ['season', 'defense'])
        drive_df = drive_df.merge(off_rating_df, how = 'left', on = ['season', 'offense'])
        drive_df = drive_df.merge(def_rating_df, how = 'left', on = ['season', 'defense'])
    if import_weekly_data:
        try:
            if run_on_live_connections:
                weekly_import_df = nfl.import_weekly_data(years = training_set_seasons)
            else:
                weekly_import_df = nfl_data_loader.weekly(seasons = training_set_seasons)
            weekly_df = nfl_data_py_weekly_transform_import(weekly_import_df)
            if import_custom_rating:
                weekly_df = weekly_df.merge(off_rating_df, how = 'left', on = ['season', 'offense'])
                weekly_df = weekly_df.merge(def_rating_df, how = 'left', on = ['season', 'defense'])
        except urllib.error.HTTPError as e:
            print(f"The request to nfl.import_weekly_data() returned a {e}; check whether the season values passed are supported.")

    if future_projection:
        drive_train_df = drive_df.copy()
        drive_test_df = convert_schedule_to_test_frame(schedule_df, test_split_season, test_split_week)
        drive_test_df = drive_test_df.merge(off_rating_df, how = 'left', on = ['season', 'offense'])
        drive_test_df = drive_test_df.merge(def_rating_df, how = 'left', on = ['season', 'defense'])
        target_in_test_set = False
    else:        
        drive_train_df = drive_df[~((drive_df['season'] == test_split_season) & (drive_df['week'] > test_split_week))].copy()
        drive_test_df = drive_df[((drive_df['season'] == test_split_season) & (drive_df['week'] > test_split_week))].copy()
        target_in_test_set = True
        
    drive_target = 'drive_result'
    drive_outcome_pipeline = build_multinomial_log_reg_pipeline(train_set = drive_train_df, 
                                                                target = drive_target, 
                                                                numeric_features = ['offense_rating', 'defense_rating'], 
                                                                one_hot_features = ['home_team_on_offense'])
    test_output_df = project_multinomial_test_set(drive_outcome_pipeline, drive_test_df, drive_target, target_in_test_set)

    if target_in_test_set:
        classification_results_report, log_loss_score = create_multinomial_metrics_report(drive_outcome_pipeline, drive_test_df, drive_target)
        print(classification_results_report)
        print(f"The log-loss score is {log_loss_score}")
        game_projection_df = test_output_df
    else:
        game_projection_df = convert_test_output_to_game_outcomes(test_output_df, drive_train_df)
    
    return pbp_df, drive_df, game_projection_df


if __name__ == "__main__":
    model_start_time = datetime.now()
    pbp_df, drive_df, game_projection_df = nfl_model_v4(future_projection=True, 
                                                 training_set_seasons=[2023, 2024, 2025], 
                                                 test_split_season=2025,
                                                 test_split_week=9,
                                                 import_weekly_data=False,
                                                 import_custom_rating=True,
                                                 run_on_live_connections=False)
    pbp_df.to_csv("csv_output/pbp_df.csv", index=False)
    drive_df.to_csv("csv_output/drive_df.csv", index=False)
    game_projection_df.to_csv("csv_output/game_projection_df.csv", index=False)
    model_end_time = datetime.now()
    print(f"The model run time came in at {model_end_time - model_start_time}")
    
