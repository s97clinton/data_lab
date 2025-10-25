import glob
import pandas as pd

def import_single_nfl_week_input(nfl_season: int, nfl_week: int, merge_supplementary: bool) -> pd.DataFrame:
    """
    Function:
    - Imports a single week's NFL data for a given season and merges it with the data in
    the supplementary data file, which contains data for all plays; the function includes
    error handling that will return an empty DataFrame if either the weekly "frame" level
    data or the supplementary "play" level data fail to import.

    Parameters:
    <nfl_season> (int): The NFL season year.
    <nfl_week> (int): The week number.
    <merge_supplementary> (bool): Whether to merge the weekly data with the supplementary data.

    Returns:
    <df> (Pandas DataFrame): DataFrame containing the week's NFL data.
    """
    weekly_data_path = f"nfl_analytics_data/train/input_{nfl_season}_w{nfl_week:02d}.csv"
    supp_data_path = "nfl_analytics_data/supplementary_data.csv"
    try:
        df = pd.read_csv(weekly_data_path)
        print(f"✓ {nfl_season} Week {nfl_week} data: {df.shape[0]:,} play frames loaded")
    except Exception as e:
        print(f"✗ {nfl_season} Week {nfl_week} data loading failed: {e}")
        return pd.DataFrame()
    if merge_supplementary:
        try:
            supp_df = pd.read_csv(supp_data_path, dtype={25: "boolean"})
            print(f"✓ Supplementary data: {supp_df.shape[0]:,} plays loaded")
        except Exception as e:
            print(f"✗ Supplementary data loading failed: {e}")
            return pd.DataFrame()
        try:
            df = df.merge(supp_df, how="left", on=("game_id", "play_id"))
            print(f"✓ Merged data: {df.shape[0]:,} play frames after merging with supplementary data")
        except Exception as e:
            print(f"✗ Data merging failed: {e}")
            return pd.DataFrame()
        return df
    return df

def import_single_nfl_week_output(nfl_season: int, nfl_week: int) -> pd.DataFrame:
    """
    Function:
    - Imports a single week's NFL data for a given season and merges it with the data in
    the supplementary data file, which contains data for all plays; the function includes
    error handling that will return an empty DataFrame if the weekly "frame" level
    data fails to import.

    Parameters:
    <nfl_season> (int): The NFL season year.
    <nfl_week> (int): The week number.

    Returns:
    <df> (Pandas DataFrame): DataFrame containing the week's NFL data.
    """
    weekly_data_path = f"nfl_analytics_data/train/output_{nfl_season}_w{nfl_week:02d}.csv"
    try:
        df = pd.read_csv(weekly_data_path)
        print(f"✓ {nfl_season} Week {nfl_week} data: {df.shape[0]:,} play frames loaded")
    except Exception as e:
        print(f"✗ {nfl_season} Week {nfl_week} data loading failed: {e}")
        return pd.DataFrame()
    return df

def import_all_nfl_weeks_input(merge_supplementary: bool) -> pd.DataFrame:
    """
    Function:
    - Imports all NFL week data files containing 'input_' in the filename and concatenates them into a single DataFrame; 
    this data is then merged with the data in the supplementary data file, which contains data for all plays; 
    the function includes error handling that will return an empty DataFrame if either the weekly "frame" level
    data or the supplementary "play" level data fail to import.

    Parameters:
    <merge_supplementary> (bool): Whether to merge the weekly data with the supplementary data.

    Returns:
    <df> (Pandas DataFrame): DataFrame containing all weeks' NFL input data merged with supplementary data.
    """
    weekly_data_path_pattern = "nfl_analytics_data/train/input_*.csv"
    supp_data_path = "nfl_analytics_data/supplementary_data.csv"
    try:
        weekly_files = glob.glob(weekly_data_path_pattern)
        if not weekly_files:
            raise FileNotFoundError("No weekly input data files found.")
        print(f"✓ Found {len(weekly_files)} weekly input data files.")
        weekly_dfs = []
        for file in weekly_files:
            weekly_df = pd.read_csv(file)
            weekly_dfs.append(weekly_df)
        df = pd.concat(weekly_dfs, ignore_index=True)
        print(f"✓ All weeks data: {df.shape[0]:,} play frames loaded")
    except Exception as e:
        print(f"✗ Weekly data loading failed: {e}")
        return pd.DataFrame()
    if merge_supplementary:
        try:
            supp_df = pd.read_csv(supp_data_path, dtype={25: "boolean"})
            print(f"✓ Supplementary data: {supp_df.shape[0]:,} plays loaded")
        except Exception as e:
            print(f"✗ Supplementary data loading failed: {e}")
            return pd.DataFrame()
        try:
            df = df.merge(supp_df, how="left", on=("game_id", "play_id"))
            print(f"✓ Merged data: {df.shape[0]:,} play frames after merging with supplementary data")
        except Exception as e:
            print(f"✗ Data merging failed: {e}")
            return pd.DataFrame()
        return df
    else:
        return df

def import_all_nfl_weeks_output() -> pd.DataFrame:
    """
    Function:
    - Imports all NFL week data files containing 'output_' in the filename and concatenates them into a single DataFrame; 
    the function includes error handling that will return an empty DataFrame if the weekly "frame" level
    data fails to import.

    Parameters:
    -None

    Returns:
    <df> (Pandas DataFrame): DataFrame containing all weeks' NFL output data.
    """
    weekly_data_path_pattern = "nfl_analytics_data/train/output_*.csv"
    try:
        weekly_files = glob.glob(weekly_data_path_pattern)
        if not weekly_files:
            raise FileNotFoundError("No weekly output data files found.")
        print(f"✓ Found {len(weekly_files)} weekly output data files.")
        weekly_dfs = []
        for file in weekly_files:
            weekly_df = pd.read_csv(file)
            weekly_dfs.append(weekly_df)
        df = pd.concat(weekly_dfs, ignore_index=True)
        print(f"✓ All weeks data: {df.shape[0]:,} play frames loaded")
        return df
    except Exception as e:
        print(f"✗ Weekly data loading failed: {e}")
        return pd.DataFrame()

def import_plays_data_input() -> pd.DataFrame:
    """
    Function:
    - Imports all NFL week data files containing 'input_' in the filename and concatenates them into a single DataFrame,
    then drops duplicate play entries to create a DataFrame with unique plays; 
    this data is then merged with the data in the supplementary data file, which contains data for all plays; 
    the function includes error handling that will return an empty DataFrame if either the weekly "frame" level
    data or the supplementary "play" level data fail to import.

    Parameters:
    - None

    Returns:
    <df> (Pandas DataFrame): DataFrame containing all weeks' NFL input data merged with supplementary data.
    """
    weekly_data_path_pattern = "nfl_analytics_data/train/input_*.csv"
    supp_data_path = "nfl_analytics_data/supplementary_data.csv"
    try:
        weekly_files = glob.glob(weekly_data_path_pattern)
        if not weekly_files:
            raise FileNotFoundError("No weekly input data files found.")
        print(f"✓ Found {len(weekly_files)} weekly input data files.")
        weekly_dfs = []
        for file in weekly_files:
            weekly_df = pd.read_csv(file)
            weekly_df = weekly_df[['game_id', 'play_id']].drop_duplicates()
            weekly_dfs.append(weekly_df)
        df = pd.concat(weekly_dfs, ignore_index=True)
        print(f"✓ All weeks data: {df.shape[0]:,} play frames loaded")
    except Exception as e:
        print(f"✗ Weekly data loading failed: {e}")
        return pd.DataFrame()
    try:
        supp_df = pd.read_csv(supp_data_path, dtype={25: "boolean"})
        print(f"✓ Supplementary data: {supp_df.shape[0]:,} plays loaded")
    except Exception as e:
        print(f"✗ Supplementary data loading failed: {e}")
        return pd.DataFrame()
    try:
        df = df.merge(supp_df, how="left", on=("game_id", "play_id"))
        print(f"✓ Merged data: {df.shape[0]:,} play frames after merging with supplementary data")
    except Exception as e:
        print(f"✗ Data merging failed: {e}")
        return pd.DataFrame()
    return df