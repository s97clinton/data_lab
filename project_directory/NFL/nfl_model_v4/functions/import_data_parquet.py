import pandas as pd
from typing import Optional

class NFLDataLoader:
    """
    Class:
    -Loader for local NFL parquet data sourced from nfl_data_py. 
    Centralizes importing and concatenatin season-level files.
    -Uses the "walrus operator ( := ) " to verify the dataframe expected
    at a particular path "is not None" in a single line; requires Python 3.8+.

    Example:
        >>> loader = NFLDataLoader()
        >>> pbp_df = loader.pbp([2021, 2022])
    """
    def __init__(self, base_path: str = "data_nfl_data_py_parquets"):
        """
        Function:
        -Initialize with root data directory.
        """
        self.base_path = base_path

    def _load_season(self, season: int, subdir: str, filename: str) -> Optional[pd.DataFrame]:
        """
        Function
        -Load a single parquet file.
        """
        path = f"{self.base_path}/{subdir}/{filename}_{season}.parquet"
        try:
            return pd.read_parquet(path)
        except Exception:
            print(f"File not found: {path}")
            return None
        
    def _load_seasons(self, seasons: list[int], subdir: str, filename: str) -> Optional[pd.DataFrame]:
        """
        Function
        -Load and concatenate parquet files.
        """
        dfs = [
            df for season in seasons if (df := self._load_season(season, subdir, filename)) is not None
        ]
        return pd.concat(dfs, axis=0) if dfs else None
    
    def pbp(self, seasons: list[int]) -> Optional[pd.DataFrame]:
        """
        Function
        -Load play-by-play data.
        """
        return self._load_seasons(seasons, "nfl_pbp_data", "nfl_pbp_data")
    
    def schedule(self, seasons: list[int]) -> Optional[pd.DataFrame]:
        """
        Function
        -Load schedule data.
        """
        return self._load_seasons(seasons, "nfl_schedules", "nfl_schedule")
    
    def weekly(self, seasons: list[int]) -> Optional[pd.DataFrame]:
        """
        Function
        -Load weekly data.
        """
        return self._load_seasons(seasons, "nfl_weekly_data", "nfl_weekly_data")

