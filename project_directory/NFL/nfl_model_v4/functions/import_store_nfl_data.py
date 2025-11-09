import nfl_data_py as nfl

def store_nfl_data_py_schedule_parquet(seasons: list[int]) -> None:
    """
    Function
    -Takes a list of seasons (or to update only current season, a list of one season),
    and stores the schedule for each season in a seperate parquet file.

    Parameters:
    <seasons> (list of int): NFL seasons to pull and store schedule.

    Returns:
    None, stores data in parquet files.
    """
    df = nfl.import_schedules(seasons)
    for season in seasons:
        season_df = df[df['season']==season].copy()
        season_df.to_parquet(f'data_nfl_data_py_parquets/nfl_schedules/nfl_schedule_{season}.parquet')
    
    return None

def store_nfl_data_py_pbp_data_parquet(seasons: list[int]) -> None:
    """
    Function
    -Takes a list of seasons (or to update only current season, a list of one season),
    and stores the play-by-play data for each season in a seperate parquet file.

    Parameters:
    <seasons> (list of int): NFL seasons to pull and store pbp data.

    Returns:
    None, stores data in parquet files.
    """
    df = nfl.import_pbp_data(seasons)
    for season in seasons:
        season_df = df[df['season']==season].copy()
        season_df.to_parquet(f'data_nfl_data_py_parquets/nfl_pbp_data/nfl_pbp_data_{season}.parquet')
    
    return None

def store_nfl_data_py_weekly_data_parquet(seasons: list[int]) -> None:
    """
    Function
    -Takes a list of seasons (or to update only current season, a list of one season),
    and stores the weekly player data for each season in a seperate parquet file.

    Parameters:
    <seasons> (list of int): NFL seasons to pull and store weekly player data.

    Returns:
    None, stores data in parquet files.
    """
    df = nfl.import_weekly_data(seasons)
    for season in seasons:
        season_df = df[df['season']==season].copy()
        season_df.to_parquet(f'data_nfl_data_py_parquets/nfl_weekly_data/nfl_weekly_data_{season}.parquet')
    
    return None

