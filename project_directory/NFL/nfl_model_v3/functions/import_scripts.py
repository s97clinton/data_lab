import os
import pandas as pd
from functions.utils import create_nfl_engine

def import_schedule_csv(season):
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
        df = pd.read_csv("nfl_model_v3/data_files/schedules/2024FullSeasonSchedule.csv")
        df['season'] = 2024
        df = df.rename(columns={'Week': 'week', 'Date': 'date', 'Away': 'away', 'Home': 'home'})
        df = df[['season','week','date','away','home']]
    else:
        print("Error: No NFL schedule for specified season found in directory.")
    
    return df

def import_historic_rating(start_season, current_season):
    """
    Function:
    -Imports the NFL Team Ratings from data_files based on parameters
    provided (<start_season>, <current_season>)

    Parameters:
    <start_season> (int): Initial Season to import NFL Team Ratings
    <current_season> (int): Final Season to import NFL Team Ratings

    Returns:
    <rating_df> (DataFrame): Combined Offensive and Defensive Ratings
    """
    base_path = "nfl_model_v3/data_files/dvoa_historic"
    seasons = list(range(start_season, current_season))
    offense_dfs = []
    defense_dfs = []
    
    for season in seasons:
        offense_file = os.path.join(base_path, f"{season} Team DVOA Ratings Offense.csv")
        if os.path.exists(offense_file):
            df_off = pd.read_csv(offense_file)
            df_off['Season'] = season
            df_off['Team'] = df_off['Team'].replace({'LV': 'LVR', 'OAK': 'LVR', 'WAS': 'WSH'})
            df_off = df_off[['Team', 'Season', 'Weighted DVOA']].rename(columns={'Weighted DVOA': 'Off_DVOA'})
            offense_dfs.append(df_off)
        
        defense_file = os.path.join(base_path, f"{season} Team DVOA Ratings Defense.csv")
        if os.path.exists(defense_file):
            df_def = pd.read_csv(defense_file)
            df_def['Season'] = season
            df_def['Team'] = df_def['Team'].replace({'LV': 'LVR', 'OAK': 'LVR', 'WAS': 'WSH'})
            df_def = df_def[['Team', 'Season', 'Weighted DVOA']].rename(columns={'Weighted DVOA': 'Def_DVOA'})
            defense_dfs.append(df_def)
    
    off_df = pd.concat(offense_dfs, ignore_index=True) if offense_dfs else pd.DataFrame()
    def_df = pd.concat(defense_dfs, ignore_index=True) if defense_dfs else pd.DataFrame()
    rating_df = pd.merge(off_df, def_df, on=['Team', 'Season'], how='inner')
    
    rating_df['Off_DVOA'] = pd.to_numeric(rating_df['Off_DVOA'].str.replace('%', '', regex=True)) / 100
    rating_df['Def_DVOA'] = pd.to_numeric(rating_df['Def_DVOA'].str.replace('%', '', regex=True)) / 100
    rating_df = rating_df.rename(columns={'Team': 'team', 'Season': 'season', 'Off_DVOA': 'off_rating', 'Def_DVOA': 'def_rating'})
    
    return rating_df

def import_current_rating(current_season, current_week):
    """
    Function:
    -Import the current_rating for offenses and defenses in the current week;
    the Pandas Dataframe returned should match the format of the Dataframe returned
    by import_historic_rating function.

    Parameters:
    <current_season> (int): Season to import NFL Team Ratings
    <current_week> (int): Week to import NFL Team Ratings

    Returns:
    <rating_df> (DataFrame): Combined Offensive and Defensive Ratings
    """
    df = pd.read_csv(f"nfl_model_v3/data_files/dvoa_current/{current_season}/{current_season}_SSRating_wk{current_week}.csv")
    rating_df = df[['Team','SS OFF DVOA','SS DEF DVOA']]
    rating_df = rating_df.rename(columns={'Team': 'team', 'SS OFF DVOA': 'off_rating', 'SS DEF DVOA': 'def_rating'})
    rating_df['season'] = current_season
    rating_df = rating_df[['team','season','off_rating','def_rating']]

    return rating_df

def import_coach_qb(start_season, current_season):
    """
    Function:
    -Import the coach_qb table as a Pandas Dataframe, filter
    the Dataframe by the start_season to current_season, and
    return the Dataframe.

    Parameters:
    <start_season> (int): Initial Season to import NFL Team Ratings
    <current_season> (int): Final Season to import NFL Team Ratings

    Returns:
    <coach_qb_df> (Dataframe): Pandas DF w/ info on coaches, starting QBs
    """
    coach_qb_df = pd.read_csv("nfl_model_v3/data_files/coach_qb_table/nfl_coach_qb_table.csv")
    coach_qb_df = coach_qb_df[(coach_qb_df['season']>=start_season) & (coach_qb_df['season']<=current_season)]

    return coach_qb_df

def import_pfr_game_basic(start_season, end_season):
    """
    Function:
    -Import the data in the MySQL pfr_game_basic table for the
    specified NFL seasons.

    Parameters:
    <start_season> (int): Initial Season to import pfr_game_basic table
    <current_season> (int): Final Season to import pfr_game_basic table

    Returns:
    <pfr_game_basic> (Dataframe): Pandas Dataframe with pfr_game_basic data
    <pfr_gm_ids> (List): List of pfr_gm_ids for further queries from MySQL DB
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfrgamebasic"

    query = f"""
        SELECT * 
        FROM {table_name}
        WHERE season >= {start_season} AND season <= {end_season};
    """
    pfr_game_basic = pd.read_sql(query, nfl_engine)
    pfr_game_ids = list(pfr_game_basic['gmID'])

    return pfr_game_basic, pfr_game_ids

def import_pfr_team_stats(pfr_game_ids):
    """
    Function:
    -Import the data in the MySQL pfr_team_stats table for the
    specified NFL game IDs.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_team_stats> (Dataframe): Pandas Dataframe with pfr_team_stats data and the
    season/week from pfr_game_basic
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfrteamstats"
    secondary_table = "pfrgamebasic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week
        FROM {table_name} t
        JOIN {secondary_table} b ON t.key = b.key
        WHERE t.gmID IN ({game_ids_string});
    """

    pfr_team_stats = pd.read_sql(query, nfl_engine)

    return pfr_team_stats

def import_pfr_pass_df(pfr_game_ids):
    """
    Function:
    -Import the data in the MySQL pfrpassingbase table for the
    specified NFL game IDs.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_pass_df> (Dataframe): Pandas Dataframe with pfrpassingbase data and the
    season/week from pfr_game_basic
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfrpassingbase"
    secondary_table = "pfrgamebasic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.Opp, b.Venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.gmID = b.gmID AND t.Tm = b.Team
        WHERE t.gmID IN ({game_ids_string});
    """
    
    pfr_pass_df = pd.read_sql(query, nfl_engine)

    return pfr_pass_df

def import_pfr_pass_adv(pfr_game_ids):
    """
    Function:
    -Import the data in the MySQL pfrpassingadv table for the
    specified NFL game IDs.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_pass_adv> (Dataframe): Pandas Dataframe with pfrpassingadv data and the
    season/week from pfr_game_basic
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfrpassingadv"
    secondary_table = "pfrgamebasic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.Opp, b.Venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.gmID = b.gmID AND t.Tm = b.Team
        WHERE t.gmID IN ({game_ids_string});
    """
    
    pfr_pass_adv = pd.read_sql(query, nfl_engine)

    return pfr_pass_adv

def import_pfr_rush_df(pfr_game_ids):
    """
    Function:
    -Import the data in the MySQL pfrrushingbase table for the
    specified NFL game IDs.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_rush_df> (Dataframe): Pandas Dataframe with pfrrushingbase data and the
    season/week from pfr_game_basic
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfrrushingbase"
    secondary_table = "pfrgamebasic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.Opp, b.Venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.gmID = b.gmID AND t.Tm = b.Team
        WHERE t.gmID IN ({game_ids_string});
    """
    
    pfr_rush_df = pd.read_sql(query, nfl_engine)

    return pfr_rush_df

def import_pfr_rush_adv(pfr_game_ids):
    """
    Function:
    -Import the data in the MySQL pfrrushingadv table for the
    specified NFL game IDs.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_rush_adv> (Dataframe): Pandas Dataframe with pfrrushingadv data and the
    season/week from pfr_game_basic
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfrrushingadv"
    secondary_table = "pfrgamebasic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.Opp, b.Venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.gmID = b.gmID AND t.Tm = b.Team
        WHERE t.gmID IN ({game_ids_string});
    """
    
    pfr_rush_adv = pd.read_sql(query, nfl_engine)

    return pfr_rush_adv

def import_pfr_rec_df(pfr_game_ids):
    """
    Function:
    -Import the data in the MySQL pfrreceivingbase table for the
    specified NFL game IDs.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_rec_df> (Dataframe): Pandas Dataframe with pfrreceivingbase data and the
    season/week from pfr_game_basic
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfrreceivingbase"
    secondary_table = "pfrgamebasic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.Opp, b.Venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.gmID = b.gmID AND t.Tm = b.Team
        WHERE t.gmID IN ({game_ids_string});
    """
    
    pfr_rec_df = pd.read_sql(query, nfl_engine)

    return pfr_rec_df

def import_pfr_rec_adv(pfr_game_ids):
    """
    Function:
    -Import the data in the MySQL pfrreceivingadv table for the
    specified NFL game IDs.

    Parameters:
    <pfr_game_ids> (list): List of pfr_game_ids to refrence pulling from MySQL DB

    Returns:
    <pfr_rec_adv> (Dataframe): Pandas Dataframe with pfrreceivingadv data and the
    season/week from pfr_game_basic
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfrreceivingadv"
    secondary_table = "pfrgamebasic"

    game_ids_string = ', '.join(f"'{game_id}'" for game_id in pfr_game_ids)

    query = f"""
        SELECT t.*, b.season, b.week, b.Opp, b.Venue
        FROM {table_name} t
        JOIN {secondary_table} b on t.gmID = b.gmID AND t.Tm = b.Team
        WHERE t.gmID IN ({game_ids_string});
    """
    
    pfr_rec_adv = pd.read_sql(query, nfl_engine)

    return pfr_rec_adv

def import_pfr_drive_info(start_season, end_season):
    """
    Function:
    -Import the data in the MySQL pfr_drive_info table for the
    specified NFL seasons.

    Parameters:
    <start_season> (int): Initial Season to import pfr_drive_info table
    <current_season> (int): Final Season to import pfr_drive_info table

    Returns:
    <pfr_drive_info> (Dataframe): Pandas Dataframe with pfr_drive_info data
    """
    nfl_engine = create_nfl_engine()
    table_name = "pfrdriveinfo"

    query = f"""
        SELECT * 
        FROM {table_name}
        WHERE season >= {start_season} AND season <= {end_season};
    """
    pfr_drive_info = pd.read_sql(query, nfl_engine)

    return pfr_drive_info

def run_nfl_data_import(start_season, current_season):
    """
    Function: 
    -This function will run the full set of NFL import
    scripts according to the <start_season> and <end_season>
    parameters supplied.

    Parameters:
    <start_season> (int): Initial Season to import NFL Data for Modeling
    <current_season> (int): Final Season to import NFL Data for Modeling

    Returns:
    <nfl_schedule> (Pandas Dataframe): Pandas Dataframe w/ NFL schedule for future projections
    <hist_rating_df> (Pandas Dataframe): Pandas Dataframe w/ hist_rating_df data
    <coach_qb_df> (Pandas Dataframe): Pandas Dataframe w/ coach_qb_df data
    <pfr_game_basic> (Pandas Dataframe): Pandas Dataframe w/ pfr_game_basic data
    <pfr_team_stats> (Pandas Dataframe): Pandas Dataframe w/ pfr_team_stats data
    <pfr_pass_df> (Pandas Dataframe): Pandas Dataframe w/ pfr_pass_df data
    <pfr_rush_df> (Pandas Dataframe): Pandas Dataframe w/ pfr_rush_df data
    <pfr_rec_df> (Pandas Dataframe): Pandas Dataframe w/ pfr_rec_df data
    <pfr_drive_df> (Pandas Dataframe): Pandas Dataframe w/ pfr_drive_df data
    """
    nfl_schedule = import_schedule_csv(season = current_season)
    hist_rating_df = import_historic_rating(start_season, current_season)
    coach_qb_df = import_coach_qb(start_season, current_season)

    pfr_game_basic, pfr_game_ids = import_pfr_game_basic(start_season, current_season)
    pfr_team_stats = import_pfr_team_stats(pfr_game_ids)
    pfr_pass_df = import_pfr_pass_df(pfr_game_ids)
    pfr_rush_df = import_pfr_rush_df(pfr_game_ids)
    pfr_rec_df = import_pfr_rec_df(pfr_game_ids)

    pfr_drive_df = import_pfr_drive_info(start_season, current_season)

    return nfl_schedule, hist_rating_df, coach_qb_df,  pfr_game_basic, pfr_team_stats, pfr_pass_df, pfr_rush_df, pfr_rec_df, pfr_drive_df

