from functions.import_store_nfl_data import store_nfl_data_py_schedule_parquet, store_nfl_data_py_pbp_data_parquet, store_nfl_data_py_weekly_data_parquet

def run_nfl_data_py_update(seasons: list[int], weekly: bool=False) -> None:
    """
    Function
    -Run multiple "import and store" functions for nfl_data_py.

    Parameters:
    <seasons> (list of int): NFL seasons to pull and store schedule.

    Returns:
    None, stores data in parquet files.
    """
    store_nfl_data_py_schedule_parquet(seasons)
    store_nfl_data_py_pbp_data_parquet(seasons)
    if weekly:
        store_nfl_data_py_weekly_data_parquet(seasons)
    return None

if __name__ == "__main__":
    run_nfl_data_py_update([2025])