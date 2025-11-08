import pandas as pd
from typing import Tuple

def import_historic_rating() -> Tuple:
    """
    Function:
    -Imports the historic NFL Team Ratings from data_files

    Parameters:
    -None, imports full .csv

    Returns:
    <hist_off_rating_df> (DataFrame): Custom Offensive Ratings Ready to Merge
    <hist_def_rating_df> (DataFrame): Custom Defensive Ratings Ready to Merge
    """
    df = pd.read_csv("data_files/team_rating_historic/team_rating_historic.csv")
    df[['team']] = df[['team']].replace('LVR', 'LV')
    df[['team']] = df[['team']].replace('WSH', 'WAS')
    df.drop(columns=['offense_rank','defense_rank'], inplace=True)
    hist_off_rating_df = df.rename(columns={'team': 'offense'}).copy()
    hist_off_rating_df.drop(columns=['defense_rating'], inplace=True)
    hist_def_rating_df = df.rename(columns={'team': 'defense'}).copy()
    hist_def_rating_df.drop(columns=['offense_rating'], inplace=True)

    return hist_off_rating_df, hist_def_rating_df

def import_current_rating() -> Tuple:
    """
    Function:
    -Import the current_rating for offenses and defenses.

    Parameters:
    -None, imports full .csv

    Returns:
    <current_off_rating_df> (DataFrame): Custom Offensive Ratings Ready to Merge
    <current_def_rating_df> (DataFrame): Custom Defensive Ratings Ready to Merge
    """
    df = pd.read_csv(f"data_files/team_rating_current/current_team_rating.csv")
    df[['team']] = df[['team']].replace('LVR', 'LV')
    df[['team']] = df[['team']].replace('WSH', 'WAS')
    current_off_rating_df = df.rename(columns={'team': 'offense'}).copy()
    current_off_rating_df.drop(columns=['defense_rating'], inplace=True)
    current_def_rating_df = df.rename(columns={'team': 'defense'}).copy()
    current_def_rating_df.drop(columns=['offense_rating'], inplace=True)

    return current_off_rating_df, current_def_rating_df

def import_custom_ratings() -> Tuple:
    """
    Function:
    -Call the import_historic_rating() and import_current_rating() functions,
    ensure that the seasons in respective files line up, and concatenate into
    <off_rating_df> and <def_rating_df> that are ready to merge w/ NFL data.

    Parameters:
    -None

    Returns:
    <off_rating_df> (DataFrame): Custom Offensive Ratings Ready to Merge
    <def_rating_df> (DataFrame): Custom Defensive Ratings Ready to Merge
    """
    hist_off_rating_df, hist_def_rating_df = import_historic_rating()
    current_off_rating_df, current_def_rating_df = import_current_rating()
    if (set(hist_off_rating_df.columns) == set(current_off_rating_df)) and (hist_off_rating_df['season'].max() not in current_off_rating_df['season'].values):
        off_rating_df = pd.concat([hist_off_rating_df, current_off_rating_df], axis=0, ignore_index=True)
    if (set(hist_def_rating_df.columns) == set(current_def_rating_df)) and (hist_def_rating_df['season'].max() not in current_def_rating_df['season'].values):
        def_rating_df = pd.concat([hist_def_rating_df, current_def_rating_df], axis=0, ignore_index=True)
    
    return off_rating_df, def_rating_df