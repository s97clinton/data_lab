import nflreadpy as nfl
import os

class NFLReadPyAcquireStore:
    """
    Class
    -Class to acquire NFL data via nflreadpy package and stores in local parquet files.
    -Note: The 'depth_chart' option only runs up until 2024; nflreadpy changed the
    formatting significantly for 2025.

    Example:
        >>> store = NFLDataPyAcquireStore()
        >>> store.schedule([2021, 2022])
        >>> store.pbp([2021, 2022])
        >>> store.player_weekly([2021, 2022])
    """
    def __init__(self, base_path: str = "data_nfl_read_py_parquets"):
        """
        Function: Initialize with root data storage directory.
        """
        self.base_path = base_path
        # Define the data type configs: (import_func, subdir, filename_prefix)
        self._data_configs = {
            'schedule': (nfl.load_schedules, 'nfl_schedules', 'nfl_schedule'),
            'pbp': (nfl.load_pbp, 'nfl_pbp_data', 'nfl_pbp_data'),
            'player_weekly': (nfl.load_player_stats, 'nfl_player_weekly_data', 'nfl_player_weekly_data'),
            'team_weekly': (nfl.load_team_stats, 'nfl_team_weekly_data', 'nfl_team_weekly_data'),
            'depth_chart': (nfl.load_depth_charts, 'nfl_depth_charts', 'nfl_depth_charts')
        }

    def _ensure_dir(self, path: str) -> None:
        """Function: Create Directory if it does not exist"""
        os.makedirs(path, exist_ok=True)

    def _acquire_and_store(self, data_type: str, seasons: list[int]) -> None:
        """Function: Generic method to acquire and store data for a given type."""
        if data_type not in self._data_configs:
            raise ValueError(f"Unsupported data type: {data_type}. Choose from {list(self._data_config.keys())}")
        
        import_func, subdir, prefix = self._data_configs[data_type]
        df_polars = import_func(seasons)
        df = df_polars.to_pandas()
        full_subdir = os.path.join(self.base_path, subdir)
        self._ensure_dir(full_subdir)

        for season in seasons:
            season_df = df[df['season'] == season].copy()
            filename = f"{prefix}_{season}.parquet"
            filepath = os.path.join(full_subdir, filename)
            season_df.to_parquet(filepath)
            print(f"Saved {data_type} for season {season} to {filepath}")

    def schedule(self, seasons: list[int]) -> None:
        """Function: Store schedule data for given seasons."""
        self._acquire_and_store('schedule', seasons)
    def pbp(self, seasons: list[int]) -> None:
        """Function: Store play-by-play data for given seasons."""
        self._acquire_and_store('pbp', seasons)
    def player_weekly(self, seasons: list[int]) -> None:
        """Function: Store weekly player data for given seasons."""
        self._acquire_and_store('player_weekly', seasons)
    def team_weekly(self, seasons: list[int]) -> None:
        """Function: Store weekly team data for given seasons."""
        self._acquire_and_store('team_weekly', seasons)
    def depth_chart(self, seasons: list[int]) -> None:
        """Function: Store weekly team data for given seasons."""
        self._acquire_and_store('depth_chart', seasons)

    
def acquire_updated_depth_chart(seasons: list[int]) -> None:
    """
    Function: Acquire nflreadpy's updated depth chart for
    seasons starting in 2025; all previous seasons should be
    acquired using the NFLReadPyAcquireStore class.
    """
    for season in seasons:
        pol_depth = nfl.load_depth_charts([season])
        depth = pol_depth.to_pandas()
        depth.to_parquet(f"data_nfl_read_py_parquets/nfl_depth_charts_updated_version/depth_chart_updated_version_{season}.parquet")
        print(f"Saved updated depth chart for season {season}")
    return None