import pandas as pd
import numpy as np
from functions.utils import calculate_generic_yardline

def update_team_abbreviations(df: pd.DataFrame, old_abbv: str, new_abbv: str) -> pd.DataFrame:
    """
    Function:
    -This function will update the abbreviations for a given team in an nfl_data_py
    pbp dataframe, <df>; the three columns impacted are 'game_id', 'posteam', and 'defteam'.
    -This function should be applied before any other transformations using those three columns.

    Parameters:
    <df> (Pandas DataFrame): DataFrame of play-by-play data.

    Returns:
    <df> (Pandas DataFrame): Updated DataFrame
    """
    df['game_id'] = df['game_id'].apply(lambda x: x.replace(f'_{old_abbv}_', f'_{new_abbv}_') if old_abbv in x.split('_') else x)
    df['game_id'] = df['game_id'].apply(lambda x: x.replace(f'_{old_abbv}', f'_{new_abbv}') if old_abbv in x.split('_') else x) 
    df['posteam'] = df['posteam'].replace(old_abbv, new_abbv)
    df['defteam'] = df['defteam'].replace(old_abbv, new_abbv)

    return df

def set_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function will update the data types for the ['season', 'week', 'qtr', 'down'] columns
    in an nfl_data_py pbp Dataframe, df.

    Parameters:
    <df> (Pandas DataFrame): DataFrame of play-by-play data.

    Returns:
    <df> (Pandas DataFrame): Updated DataFrame
    """
    df['qtr'] = df['qtr'].astype(float)
    df['season'] = df['season'].astype(int)
    df['week'] = df['week'].astype(int)
    df['down'] = df['down'].astype('category')

    return df

def process_penalty_types(df:pd.DataFrame) -> pd.DataFrame:
    """
    Helper Function to a helper function:
    -Create new penalty classifications in nfl_data_py play-by-play.
    
    Parameters:
    <df> (Pandas Dataframe): Dataframe of nfl play-by-play data with pre-defined penalty
    field names for these operations to work on.
    
    Returns:
    <df> (Pandas Dataframe): Updated Dataframe
    """
    penalty_types_dead_ball = ['False Start','Delay of Game','Defensive Delay of Game','Defensive Pass Interference','Delay of Kickoff','Encroachment','Neutral Zone Infraction']
    penalty_types_either_or = ['Defensive Too Many Men on Field','Illegal Substitution','Offensive Too Many Men on Field']
    
    df['penalty_dead_ball_no_play'] = np.where((df['play_type'] == 'no_play') & (df['penalty_type'].isin(penalty_types_dead_ball)) & (df['penalty'] == 1.0), 1.0, 0.0)
    df['penalty_unknown_no_play'] = np.where((df['play_type'] == 'no_play') & (df['penalty_type'].isin(penalty_types_either_or)) & (df['penalty'] == 1.0), 1.0, 0.0)
    df['penalty_live_snap_no_play'] = np.where((df['play_type'] == 'no_play') & ~(df['penalty_type'].isin(penalty_types_dead_ball + penalty_types_either_or))  & (df['penalty'] == 1.0), 1.0, 0.0)
    
    return df

def simple_column_creation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function will perform basic operations to create
    basic supplementary columns; more advanced feature creation
    is done downstream.

    Parameters:
    <df> (Pandas DataFrame): DataFrame of play-by-play data.

    Returns:
    <df> (Pandas DataFrame): Updated DataFrame
    """
    new_columns = pd.DataFrame({
        'half': np.select(
            [df['qtr'].isin([1.0, 2.0]), df['qtr'].isin([3.0, 4.0])],
            [1, 2],
            default=3
        ).astype(int),
        'home_team_on_offense': df['posteam_type'] == 'home',
        'offense': df['posteam'],
        'defense': df['defteam'],
        'yardline': 100 - df['yardline_100'],
        'backed_up': np.where((100 - df['yardline_100']) <= 15, np.log(16 - (100 - df['yardline_100'])), 0)
    })
    df = pd.concat([df, new_columns], axis=1)

    return df

def _update_drive_result_nfl_data_py_pbp(row: pd.Series) -> str:
    """
    Helper Function to a helper function:
    -This function will update nfl_data_py's "drive_result" field with more detail
    based on other fields available in the data that provide additional context.
    
    Parameters:
    <row>: Pandas Series (row of DF) with Boolean fields indicating what happened on
    the play in question ('interception', 'pass_touchdown') and the general 'drive_result'
    
    Returns:
    <row['drive_result']>: row with updated drive_result in Pandas DF
    """    
    if row['drive_result'] == 'Turnover':
        if row['interception'] == 1.0:
            return 'interception'
        elif row['fumble_lost'] == 1.0:
            return 'lost_fumble'
        
    elif row['drive_result'] == 'Touchdown':
        if row['pass_touchdown'] == 1.0:
            return 'pass_td'
        elif row['rush_touchdown'] == 1.0:
            return 'rush_td'
        elif row['fumble_forced'] == 1.0:
            return 'off_fr_td'
        elif row['fumble_not_forced'] == 1.0:
            return 'off_fr_td'
        elif row['return_touchdown'] == 1.0 and row['play_type'] == 'kickoff':
            return 'off_kor_td'
    
    elif row['drive_result'] == 'Opp touchdown':
        if row['interception'] == 1.0:
            return 'int_opp_td'
        elif row['fumble_lost'] == 1.0:
            return 'lost_fumble_opp_td'
        elif row['punt_attempt'] == 1.0:
            return 'punt_returned_opp_td'
        elif row['field_goal_attempt'] == 1.0:
            return 'fga_returned_opp_td'
    
    return row['drive_result']

def _final_drive_result_nfl_data_py_pbp(group:pd.DataFrame) -> pd.DataFrame:
    """
    Helper Function to a helper function:
    -This function is designed to be applied AFTER the helper function 
    {_update_drive_result(row)}; that function will update the "drive_result"
    for the "row" (play) where the TD took place, but not the previous plays on the drive;
    this function will update the result for all "rows" (plays) on the drive.
    """    
    detailed_results = ['pass_td', 'rush_td', 'return_td', 'off_fr_td', 'interception', 'lost_fumble','int_opp_td','lost_fumble_opp_td','punt_returned_opp_td','fga_returned_opp_td']
    
    for result in detailed_results:
        if result in group.values:
            return result
    return group.iloc[0]

def update_column_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    - Updates the values in specified columns of nfl_data_py ['field_goal_result', 'drive_result']
    to more intuitive outputs.
    
    Parameters:
    <df> (Pandas DataFrame): DataFrame with the columns to update
    
    Returns:
    <df> (Pandas DataFrame): Updated DataFrame
    """
    df['field_goal_result'] = df['field_goal_result'].apply(lambda x: 1 if x == 'made' else 0)
    df['field_goal_result'] = df['field_goal_result'].astype(bool)
    
    df['drive_result'] = df['fixed_drive_result']
    df['drive_result'] = df.apply(_update_drive_result_nfl_data_py_pbp, axis=1)
    df['drive_result'] = df.groupby(['game_id', 'drive'])['drive_result'].transform(_final_drive_result_nfl_data_py_pbp)
    
    drive_result_replacement_dict = {
        "Field goal": "field_goal_attempt",
        "Missed field goal": "field_goal_attempt",
        "Punt": "punt",
        "Turnover on downs": "downs",
        "Safety": "safety",
        "End of half": "end_of_half",
        "lost_fumble_opp_td": "lost_fumble", 
        "fumble": "lost_fumble", 
        "int_ret_opp_td": "interception", 
        "end_of_game": "end_of_half", 
        "Turnover": "field_goal_attempt", 
        "off_fr_td": "other", 
        "punt_return_td":"punt", 
        "punt_block_safety":"punt"
    }
    df['drive_result'] = df['drive_result'].replace(drive_result_replacement_dict)

    return_td_into_play_type_replacement_dict = {
        "punt_returned_opp_td": "punt",
        "int_opp_td": "interception",
        "lost_fumble_opp_td": "lost_fumble",
        "fga_returned_opp_td": "field_goal_attempt"
    }
    df['drive_result'] = df['drive_result'].replace(return_td_into_play_type_replacement_dict)

    return df

def parse_weather_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function will parse the 'weather' column contained in
    the nfl_data_py pbp DataFrame and return an updated DataFrame.

    Parameters:
    <df> (Pandas DataFrame): DataFrame of play-by-play data.

    Returns:
    <df> (Pandas DataFrame): Updated DataFrame
    """
    df['temp'] = df['weather'].str.extract(r'Temp: (\d+)').fillna(68).astype(float)
    df['wind'] = df['weather'].str.extract(r'Wind:\s*[A-Za-z]+\s*(\d+)').fillna(0).astype(float)
    df['humidity'] = df['weather'].str.extract(r'Humidity: (\d+)%').fillna(50).astype(float)

    df.loc[df['roof'] != 'outdoors', ['temp','wind','humidity']] = 68, 0, 50
    df.loc[df['stadium'] == 'Arena Corinthians', ['temp','wind','humidity']] = 68, 0, 50
    df['indoor_conditions'] = (df['roof'] != 'outdoors').astype(bool)

    return df

def prep_nfl_data_py_pbp(pbp_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function takes a Dataframe containing play-by-play data from nfl_data_py,
    performs cleanup operations, and return a cleaned DataFrame for further modeling.

    Parameters:
    <pbp_df> (Pandas DataFrame): DataFrame of play-by-play data.

    Returns:
    <df> (Pandas DataFrame): Cleaned DataFrame of play-by-play data.
    """
    df = pbp_df.copy()
    df.rename(columns={'ydstogo': 'distance'}, inplace=True)
    df = update_team_abbreviations(df, 'LA', 'LAR')
    df = set_data_types(df)
    df = df.dropna(subset=['posteam', 'defteam', 'drive'])
    df = df.sort_values(by=['season', 'week'], ascending=[True, True])
    df = process_penalty_types(df)
    df = calculate_generic_yardline(df, 'posteam', 'drive_end_yard_line')
    df = update_column_values(df)
    df = simple_column_creation(df)
    df = parse_weather_column(df)

    df = df[df['play_type'].isin(['run', 'pass', 'qb_kneel', 'qb_spike'])]
    df = df[['game_id', 'season', 'week', 'stadium', 'roof', 'temp', 'wind', 'offense', 'defense', 'home_team_on_offense', 'half', 'qtr', 'game_seconds_remaining', 'half_seconds_remaining', 'score_differential', 'posteam_score', 'drive', 'down', 'distance', 'yardline', 'drive_end_yard_line', 'goal_to_go', 'play_type', 'yards_gained', 'first_down', 'passer_id', 'passer_player_name', 'rusher_id', 'rusher_player_name', 'receiver_id', 'receiver_player_name', 'complete_pass', 'sack', 'touchdown', 'drive_result']]
    
    return df