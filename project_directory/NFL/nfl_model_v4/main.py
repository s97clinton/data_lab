import sys
import os
current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(parent_dir)

from datetime import datetime
import nfl_data_py as nfl
from functions.data_transformation import prep_nfl_data_py_pbp, filter_and_subset_nfl_data_py_pbp, nfl_data_py_pbp_to_drives, filter_and_subset_nfl_drive_df
from functions.feature_engineering import create_features_nfl_data_py
from function_library.py_predictive_modeling.model_wrappers_sci_kit_learn import multinomial_logistic_regression

def nfl_model_v4(seasons: list[int]):
    """
    Function:
    -Main function for NFL Model Version 4.

    Parameters:
    <seasons> (list[int]): A list of integers denoting the NFL seasons to include in training data.

    Returns:
    <pbp_df> (DataFrame): Temporary return to verify initial data load is working.
    <drive_df> (DataFrame): Temporary return to verify initial data load is working.s
    """
    df = nfl.import_pbp_data(years = seasons)
    base_df = prep_nfl_data_py_pbp(df)
    pbp_df = filter_and_subset_nfl_data_py_pbp(base_df)
    pbp_df = create_features_nfl_data_py(pbp_df)
    drive_df = nfl_data_py_pbp_to_drives(base_df)
    drive_df = filter_and_subset_nfl_drive_df(drive_df)
    return pbp_df, drive_df


if __name__ == "__main__":
    model_start_time = datetime.now()
    pbp_df, drive_df = nfl_model_v4([2023, 2024, 2025])
    pbp_df.to_csv("csv_output/pbp_df.csv", index=False)
    drive_df.to_csv("csv_output/drive_df.csv", index=False)
    model_end_time = datetime.now()
    print(f"The model run time came in at {model_end_time - model_start_time}")
    
