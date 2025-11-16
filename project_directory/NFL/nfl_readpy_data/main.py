from functions.acquire_store_nfl_readpy_data import NFLReadPyAcquireStore, acquire_updated_depth_chart

def run_nfl_data_py_update(seasons: list[int], weekly: bool=False, depth_chart: bool=False) -> None:
    """
    Function
    -Run multiple "import and store" functions for nfl_data_py.

    Parameters:
    <seasons> (list of int): NFL seasons to pull and store schedule.

    Returns:
    None, stores data in parquet files.
    """
    store = NFLReadPyAcquireStore()
    store.schedule(seasons)
    store.pbp(seasons)
    if weekly:
        store.player_weekly(seasons)
        store.team_weekly(seasons)
    if depth_chart:
        season_pre_2025 = [s for s in seasons if s < 2025]
        season_2025_after = [s for s in seasons if s >= 2025]
        if season_pre_2025:
            store.depth_chart(season_pre_2025)
        if season_2025_after:
            acquire_updated_depth_chart(season_2025_after)
    return None

if __name__ == "__main__":
    run_nfl_data_py_update(list(range(2025, 2026)), True, True)

