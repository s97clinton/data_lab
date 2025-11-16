from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Optional

class NFLDataLoader:
    """
    Class:
    -Loader for local NFL parquet data sourced from nfl_read_py. 
    Centralizes importing and concatenatin season-level files.

    Example:
        >>> loader = NFLDataLoader()
        >>> pbp_df = loader.pbp([2021, 2022])
    """
    def __init__(self) -> None:
        """
        Function:
        -Initialize with root data directory.
        """
        current_file = Path(__file__)
        self.base_path = (current_file.parent.parent
                          / "nfl_readpy_data"
                          / "data_nfl_read_py_parquets").resolve()

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
    
    def player_weekly(self, seasons: list[int]) -> Optional[pd.DataFrame]:
        """
        Function
        -Load weekly player data.
        """
        return self._load_seasons(seasons, "nfl_player_weekly_data", "nfl_player_weekly_data")
    
    def team_weekly(self, seasons: list[int]) -> Optional[pd.DataFrame]:
        """
        Function
        -Load weekly player data.
        """
        return self._load_seasons(seasons, "nfl_team_weekly_data", "nfl_team_weekly_data")
    
    def depth_charts(self, seasons: list[int], schedule: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Function
        -Load weekly depth chart data; takes the <schedule> to align depth chart with gamedays for seasons after 2024.
        """
        seasons_pre_2025 = [s for s in seasons if s < 2025]
        seasons_2025_after = [s for s in seasons if s >= 2025]
        if seasons_pre_2025:
            df1 = self._load_seasons(seasons_pre_2025, "nfl_depth_charts", "nfl_depth_charts")
            df1 = df1[df1['formation'] != 'Special Teams']
            df1.rename(columns={'club_code': 'team', 'gsis_id': 'player_id', 'depth_team': 'depth_rank'}, inplace=True)
            df1 = df1[['season', 'week', 'team', 'player_id', 'depth_position', 'depth_rank']]
        if seasons_2025_after:
            schedule_merge = schedule[schedule['season'] == 2025].copy()
            away_merge = schedule_merge[['gameday', 'season', 'week', 'away_team']].copy()
            away_merge.rename(columns={'away_team': 'team'}, inplace=True)
            home_merge = schedule_merge[['gameday', 'season', 'week', 'home_team']].copy()
            home_merge.rename(columns={'home_team': 'team'}, inplace=True)

            schedule_merge_df = pd.concat([away_merge, home_merge], axis=0, ignore_index=True)
            schedule_merge_df['gameday'] = pd.to_datetime(schedule_merge_df['gameday'], utc=True).dt.date
            schedule_merge_df['team'] = schedule_merge_df['team'].astype('string')

            df2 = self._load_seasons(seasons_2025_after, "nfl_depth_charts_updated_version", "depth_chart_updated_version")
            df2 = df2[df2['pos_grp'] != 'Special Teams']
            df2['dt'] = pd.to_datetime(df2['dt'], utc=True)
            df2['date'] = df2['dt'].dt.date

            df2 = df2.merge(schedule_merge_df, how='left', left_on=['team', 'date'], right_on=['team', 'gameday'])
            df2.dropna(subset=['gameday', 'season', 'week'], inplace=True)
            df2.rename(columns={'gsis_id': 'player_id', 'pos_abb': 'depth_position', 'pos_rank': 'depth_rank'}, inplace=True)
            df2 = df2[['season', 'week', 'team', 'player_id', 'depth_position', 'depth_rank']]
        if seasons_pre_2025 and seasons_2025_after:
            return pd.concat([df1, df2], axis=0, ignore_index=True)
        if seasons_pre_2025:
            return df1
        if seasons_2025_after:
            return df2
        print(f"The seasons in {seasons} did not match any qualifying years the stored data parquets")
        
