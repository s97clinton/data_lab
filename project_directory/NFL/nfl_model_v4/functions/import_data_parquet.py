import pandas as pd

def import_nfl_data_py_pbp_parquet(seasons: list[int]) -> pd.DataFrame:
    """
    Function:
    -Takes a list of seasons, imports each local parquet file by season,
    and concatenates the data in a single Pandas DataFrame.

    Parameters:
    <seasons> (list of int): NFL seasons to import.

    Returns:
    <hist_off_rating_df> (DataFrame): Data for all requested seasons.
    """
    for season in seasons:
        try:
            season_df = pd.read_parquet(f'nfl_data_py_parquet/nfl_pbp_data/nfl_pbp_data_{season}.parquet')
        except SyntaxError as e:
            print(f"No parquet file was found at the path for the requested season {season}.")
        season_df