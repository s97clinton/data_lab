from functions.acquire_store_nfl_data_py import NFLDataPyAcquireStore

def run_nfl_data_py_update(seasons: list[int], weekly: bool=False) -> None:
    """
    Function
    -Run multiple "import and store" functions for nfl_data_py.

    Parameters:
    <seasons> (list of int): NFL seasons to pull and store schedule.

    Returns:
    None, stores data in parquet files.
    """
    store = NFLDataPyAcquireStore()
    store.schedule(seasons)
    store.pbp(seasons)
    if weekly:
        store.weekly(seasons)
    return None

if __name__ == "__main__":
    run_nfl_data_py_update(list(range(2025, 2026)), False)

