import os
import pandas as pd
from functions.utils import create_nfl_engine

def import_schedule_csv(season: int) -> pd.DataFrame:
    """
    Function:
    -Imports the NFL schedule with the games to be projected
    based on parameter set.
    -This function works with a .csv file stored in nfl_model_files
    and will be deprecated once that is moved to the database.

    Parameters:
    <season> (int): Used to select the NFL season to Import

    Returns:
    <df> (Pandas Dataframe): Pandas Dataframe w/ NFL schedule data
    """
    if season == 2024:
        df = pd.read_csv("data_files/schedules/nfl_schedule_2024.csv")
        df['season'] = 2024
    elif season == 2025:
        df = pd.read_csv("data_files/schedules/nfl_schedule_2025.csv")
        df['season'] = 2025
    else:
        print("Error: No NFL schedule for specified season found in directory.")
        return None
    df = df.rename(columns={'Week': 'week', 'Date': 'date', 'Away': 'away', 'Home': 'home'})
    df = df[['season','week','date','away','home']]
    
    return df

def import_historic_rating(start_season: int, current_season: int) -> pd.DataFrame:
    """
    Function:
    -Imports the NFL Team Ratings from data_files based on parameters
    provided (<start_season>, <current_season>)

    Parameters:
    <start_season> (int): Initial Season to import data.
    <current_season> (int): Final Season to import data.

    Returns:
    <rating_df> (DataFrame): Combined Offensive and Defensive Ratings
    """
    rating_df = pd.read_csv("data_files/dvoa_historic/historic_dvoa.csv")

    rating_df['Offense_DVOA'] = pd.to_numeric(rating_df['Offense_DVOA'].str.replace('%', '', regex=True)) / 100
    rating_df['Defense_DVOA'] = pd.to_numeric(rating_df['Defense_DVOA'].str.replace('%', '', regex=True)) / 100
    rating_df.drop(columns=['Offense_DVOA_Rank','Defense_DVOA_Rank'], inplace=True)
    rating_df = rating_df.rename(columns={'Team': 'team', 'Season': 'season', 'Offense_DVOA': 'off_rating', 'Defense_DVOA': 'def_rating'})
    rating_df = rating_df[(rating_df['season']>=start_season) & (rating_df['season']<=current_season)]

    return rating_df

def import_current_rating(current_season: int, current_week: int) -> pd.DataFrame:
    """
    Function:
    -Import the current_rating for offenses and defenses in the current week;
    the Pandas Dataframe returned should match the format of the Dataframe returned
    by import_historic_rating function.

    Parameters:
    <current_season> (int): Season to import data.
    <current_week> (int): Week to import data.

    Returns:
    <rating_df> (DataFrame): Combined Offensive and Defensive Ratings
    """
    df = pd.read_csv(f"data_files/dvoa_current/{current_season}/{current_season}_SSRating_wk{current_week}.csv")
    rating_df = df[['Team','SS OFF DVOA','SS DEF DVOA']]
    rating_df = rating_df.rename(columns={'Team': 'team', 'SS OFF DVOA': 'off_rating', 'SS DEF DVOA': 'def_rating'})
    rating_df['season'] = current_season
    rating_df = rating_df[['team','season','off_rating','def_rating']]

    return rating_df

def import_coach_qb(start_season: int, current_season: int) -> pd.DataFrame:
    """
    Function:
    -Import the coach_qb table as a Pandas Dataframe, filter
    the Dataframe by the start_season to current_season, and
    return the Dataframe w/ info on coaches, starting QBs.

    Parameters:
    <start_season> (int): Initial Season to import data.
    <current_season> (int): Final Season to import data.

    Returns:
    <coach_qb_df> (Dataframe): Final Pandas Dataframe
    """
    coach_qb_df = pd.read_csv("data_files/coach_qb_table/nfl_coach_qb_table.csv")
    coach_qb_df = coach_qb_df[(coach_qb_df['season']>=start_season) & (coach_qb_df['season']<=current_season)]

    return coach_qb_df

def import_pfr_game_basic(start_season: int, end_season: int) -> pd.DataFrame:
    """
    Function:
    -Import the data in the MySQL pfr_game_basic table for the
    specified NFL seasons, return that data as a Pandas DataFrame,
    and return all 'game_id' values in that frame as a list.

    Parameters:
    <start_season> (int): Initial Season to import pfr_game_basic table
    <current_season> (int): Final Season to import pfr_game_basic table

    Returns:
    <pfr_game_basic> (Dataframe): Pandas Dataframe with pfr_game_basic data
    <pfr_gm_ids> (List): List of pfr_gm_ids for further queries from MySQL DB
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfr_game_basic"

    query = f"""
        SELECT * 
        FROM {table_name}
        WHERE season >= {start_season} AND season <= {end_season};
    """
    pfr_game_basic = pd.read_sql(query, nfl_engine)
    pfr_game_ids = list(pfr_game_basic['game_id'])

    return pfr_game_basic, pfr_game_ids

def import_pfr_team_stats(pfr_game_ids: list) -> pd.DataFrame:
    """
    Function:
    -Import the data in the MySQL pfr_team_stats table for the
    specified NFL game IDs and return Pandas Dataframe with pfr_team_stats 
    data and the season/week from pfr_game_basic.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_team_stats> (Dataframe): Final Pandas Dataframe
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfr_team_stats"
    secondary_table = "pfr_game_basic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week
        FROM {table_name} t
        JOIN {secondary_table} b ON t.key = b.key
        WHERE t.game_id IN ({game_ids_string});
    """

    pfr_team_stats = pd.read_sql(query, nfl_engine)

    return pfr_team_stats

def import_pfr_pass_df(pfr_game_ids: list) -> pd.DataFrame:
    """
    Function:
    -Import the data in the MySQL pfrpassingbase table for the
    specified NFL game IDs and return with pfrpassingbase data and the
    season/week from pfr_game_basic.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_pass_df> (Dataframe): Final Pandas Dataframe 
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfr_passing_base"
    secondary_table = "pfr_game_basic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.opp, b.venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.game_id = b.game_id AND t.team = b.team
        WHERE t.game_id IN ({game_ids_string});
    """
    
    pfr_pass_df = pd.read_sql(query, nfl_engine)

    return pfr_pass_df

def import_pfr_pass_adv(pfr_game_ids: list) -> pd.DataFrame:
    """
    Function:
    -Import the data in the MySQL pfrpassingadv table for the
    specified NFL game IDs and returns DataFrame with pfrpassingadv data and the
    season/week from pfr_game_basic.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_pass_adv> (Dataframe): Final Pandas Dataframe 
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfr_passing_adv"
    secondary_table = "pfr_game_basic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.opp, b.venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.game_id = b.game_id AND t.team = b.team
        WHERE t.game_id IN ({game_ids_string});
    """
    
    pfr_pass_adv = pd.read_sql(query, nfl_engine)

    return pfr_pass_adv

def import_pfr_rush_df(pfr_game_ids: list) -> pd.DataFrame:
    """
    Function:
    -Import the data in the MySQL pfr_rushing_base table for the
    specified NFL game IDs and returns DataFrame with pfr_rushing_base data and the
    season/week from pfr_game_basic.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_rush_df> (Dataframe): Final Pandas Dataframe 
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfr_rushing_base"
    secondary_table = "pfr_game_basic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.opp, b.venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.game_id = b.game_id AND t.team = b.team
        WHERE t.game_id IN ({game_ids_string});
    """
    
    pfr_rush_df = pd.read_sql(query, nfl_engine)

    return pfr_rush_df

def import_pfr_rush_adv(pfr_game_ids: list) -> pd.DataFrame:
    """
    Function:
    -Import the data in the MySQL pfr_rushing_adv table for the
    specified NFL game IDs and returns with pfr_rushing_adv data and the
    season/week from pfr_game_basic.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_rush_adv> (Dataframe): Final Pandas Dataframe 
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfr_rushing_adv"
    secondary_table = "pfr_game_basic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.opp, b.venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.game_id = b.game_id AND t.team = b.team
        WHERE t.game_id IN ({game_ids_string});
    """
    
    pfr_rush_adv = pd.read_sql(query, nfl_engine)

    return pfr_rush_adv

def import_pfr_rec_df(pfr_game_ids: list) -> pd.DataFrame:
    """
    Function:
    -Import the data in the MySQL pfr_receiving_base table for the
    specified NFL game IDs and returns DataFrame with pfr_receiving_base data and the
    season/week from pfr_game_basic.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_rec_df> (Dataframe): Final Pandas Dataframe 
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfr_receiving_base"
    secondary_table = "pfr_game_basic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.opp, b.venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.game_id = b.game_id AND t.team = b.team
        WHERE t.game_id IN ({game_ids_string});
    """
    
    pfr_rec_df = pd.read_sql(query, nfl_engine)

    return pfr_rec_df

def import_pfr_rec_adv(pfr_game_ids: list) -> pd.DataFrame:
    """
    Function:
    -Import the data in the MySQL pfr_receiving_adv table for the
    specified NFL game IDs and returns DataFrame with pfr_receiving_adv data and the
    season/week from pfr_game_basic.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_rec_adv> (Dataframe): Final Pandas Dataframe 
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfr_receiving_adv"
    secondary_table = "pfr_game_basic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.opp, b.venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.game_id = b.game_id AND t.team = b.team
        WHERE t.game_id IN ({game_ids_string});
    """
    
    pfr_rec_adv = pd.read_sql(query, nfl_engine)

    return pfr_rec_adv

def import_pfr_drive_info(start_season: int, end_season: int) -> pd.DataFrame:
    """
    Function:
    -Import the data in the MySQL pfr_drive_info table for the
    specified NFL seasons and returns a DataFrame with pfr_drive_info data.

    Parameters:
    <start_season> (int): Initial Season to import pfr_drive_info table
    <current_season> (int): Final Season to import pfr_drive_info table

    Returns:
    <pfr_drive_info> (Dataframe): Final Pandas Dataframe 
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfr_drive_info"

    query = f"""
        SELECT * 
        FROM {table_name}
        WHERE season >= {start_season} AND season <= {end_season};
    """
    pfr_drive_info = pd.read_sql(query, nfl_engine)

    return pfr_drive_info



