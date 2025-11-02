import pandas as pd
import numpy as np
from functions.utils import calculate_generic_yardline

def _cross_validate_column_values(df: pd.DataFrame, col_one: str, col_two: str) -> pd.DataFrame:
    """
    Helper Function to fill missing values:
    - Ensures consistency by filling missing values in either column with the existing value from the other column.
    
    Parameters:
    <df>: Pandas DataFrame with the columns to match and fill
    <col_one>, <col_two>: Columns to compare and match for filling missing values
    
    Returns:
    <df>: DataFrame with filled values for the specified columns
    """
    df = df.reset_index(drop=True)
    df.loc[df[col_one].isna() & df[col_two].notna(), col_one] = df[col_two]
    df.loc[df[col_two].isna() & df[col_one].notna(), col_two] = df[col_one]
    return df

def _process_penalty_types_nfl_data_py_pbp(df:pd.DataFrame) -> pd.DataFrame:
    """
    Helper Function to a helper function:
    -Create new penalty classifications in nfl_data_py play-by-play.
    
    Parameters:
    <pbp_df>: Pandas Dataframe of nfl play-by-play data with pre-defined penalty
    field names for these operations to work on.
    
    Returns:
    <pbp_df>: Pandas Dataframe with data cleaned as noted.
    """
    penalty_types_dead_ball = ['False Start','Delay of Game','Defensive Delay of Game','Defensive Pass Interference','Delay of Kickoff','Encroachment','Neutral Zone Infraction']
    penalty_types_either_or = ['Defensive Too Many Men on Field','Illegal Substitution','Offensive Too Many Men on Field']
    
    df['penalty_dead_ball_no_play'] = np.where((df['play_type'] == 'no_play') & (df['penalty_type'].isin(penalty_types_dead_ball)) & (df['penalty'] == 1.0), 1.0, 0.0)
    df['penalty_unknown_no_play'] = np.where((df['play_type'] == 'no_play') & (df['penalty_type'].isin(penalty_types_either_or)) & (df['penalty'] == 1.0), 1.0, 0.0)
    df['penalty_live_snap_no_play'] = np.where((df['play_type'] == 'no_play') & ~(df['penalty_type'].isin(penalty_types_dead_ball + penalty_types_either_or))  & (df['penalty'] == 1.0), 1.0, 0.0)
    
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

def nfl_data_py_update_drive_result_safety(df:pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function is designed to update "safety" outcomes to reflect intentional
    safeties and blocked punts, which create some confusion when they are marked
    as safeties in the training data.
    
    Parameters:
    <df>: Pandas DataFrame with 'drive_result' updated to lowercase/underscore syntax
    
    Returns:
    <df>: Pandas DataFrame with select records updated
    """
    df.loc[(df['game_id'] == '2022_02_ATL_LAR') & (df['drive'] == 19.0), 'drive_result'] = 'intentional_safety'
    df.loc[(df['game_id'] == '2022_03_BUF_MIA') & (df['drive'] == 16.0), 'drive_result'] = 'intentional_safety'
    df.loc[(df['game_id'] == '2022_05_NYG_GB') & (df['drive'] == 16.0), 'drive_result'] = 'intentional_safety'
    df.loc[(df['game_id'] == '2022_14_NYJ_BUF') & (df['drive'] == 20.0), 'drive_result'] = 'punt_block_safety'
    df.loc[(df['game_id'] == '2022_18_NYJ_MIA') & (df['drive'] == 18.0), 'drive_result'] = 'last_play_desperation_safety'
    df.loc[(df['game_id'] == '2023_05_BAL_PIT') & (df['drive'] == 16.0), 'drive_result'] = 'punt_block_safety'
    df.loc[(df['game_id'] == '2023_08_LAR_DAL') & (df['drive'] == 5.0), 'drive_result'] = 'punt_block_safety'
    df.loc[(df['game_id'] == '2023_18_HOU_IND') & (df['drive'] == 22.0), 'drive_result'] = 'intentional_safety'
    df.loc[(df['game_id'] == '2024_20_HOU_KC') & (df['drive'] == 17.0), 'drive_result'] = 'intentional_safety'
    
    return df

def data_cleanup_nfl_data_py_pbp(df:pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function takes the raw import from the nfl_data_py play-by-play parquet files
    and performs cleanup steps to prepare it for the modeling process.
    
    Parameters:
    <df>: Pandas Dataframe containing the raw import from nfl_data_py play-by-play
    
    Returns:
    <df>: Cleaned version of the Pandas Dataframe
    """
    df['game_id'] = df['game_id'].apply(lambda x: x.replace('_LA_', '_LAR_') if 'LA' in x.split('_') else x)
    df['game_id'] = df['game_id'].apply(lambda x: x.replace('_LA', '_LAR') if 'LA' in x.split('_') else x) 
    df['posteam'] = df['posteam'].replace('LA','LAR')
    df['defteam'] = df['defteam'].replace('LA','LAR')
    
    df['qtr'] = df['qtr'].astype(float)
    df['season'] = df['season'].astype(int)
    df['week'] = df['week'].astype(int)
    df['down'] = df['down'].astype('category')

    new_columns = pd.DataFrame({
        'half': np.select(
            [df['qtr'].isin([1.0, 2.0]), df['qtr'].isin([3.0, 4.0])],
            [1, 2],
            default=3
        ),
        'home_team_on_offense': df['posteam_type'] == 'home',
        'offense': df['posteam'],
        'defense': df['defteam']
    })
    df = pd.concat([df, new_columns], axis=1)
    
    df = df.dropna(subset=['posteam', 'defteam', 'drive'])
    df = df.sort_values(by=['season', 'week'], ascending=[True, True])
    df = _cross_validate_column_values(df, 'rusher_player_id', 'rusher_id')
    df = _process_penalty_types_nfl_data_py_pbp(df)

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
        "End of half": "end_of_half"
    }

    df['drive_result'] = df['drive_result'].replace(drive_result_replacement_dict)

    return_td_into_play_type_replacement_dict = {
        "punt_returned_opp_td": "punt",
        "int_opp_td": "interception",
        "lost_fumble_opp_td": "lost_fumble",
        "fga_returned_opp_td": "field_goal_attempt"
    }

    df['drive_result'] = df['drive_result'].replace(return_td_into_play_type_replacement_dict)
    
    df.rename(columns={'ydstogo': 'distance', 'yardline_100': 'yardline'}, inplace=True)
    
    df['yardline'] = 100 - df['yardline']
    
    df['temp'] = df['weather'].str.extract(r'Temp: (\d+)').fillna(68).astype(float)
    df['wind'] = df['weather'].str.extract(r'Wind:\s*[A-Za-z]+\s*(\d+)').fillna(0).astype(float)
    df['humidity'] = df['weather'].str.extract(r'Humidity: (\d+)%').fillna(50).astype(float)

    df.loc[df['roof'] != 'outdoors', ['temp','wind','humidity']] = 68, 0, 50
    df.loc[df['stadium'] == 'Arena Corinthians', ['temp','wind','humidity']] = 68, 0, 50
    
    df = nfl_data_py_update_drive_result_safety(df)
    df = calculate_generic_yardline(df, 'posteam', 'drive_end_yard_line')
    
    return df

def filter_subset_pbp_data(nfl_data_py_pbp_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function will filter the pbp data from nfl_data_py; it filters the "play_type" column to restrict
    to offense/defense plays (no kicks) and cuts the column selection down to return an updated DataFrame
    for further modeling.

    Parameters:
    <nfl_data_py_pbp_df> (Pandas DataFrame): Output for selected seasons from nfl_data_py.

    Returns:
    <df> (Pandas DataFrame): Updated Version of the DataFrame.
    """
    df = nfl_data_py_pbp_df.copy()
    df = df[df['play_type'].isin(['run', 'pass', 'qb_kneel', 'qb_spike'])]
    df = df[['game_id', 'season', 'week', 'stadium', 'weather', 'roof', 'temp', 'wind', 'offense', 'defense', 'home_team_on_offense', 'half', 'qtr', 'game_seconds_remaining', 'half_seconds_remaining', 'score_differential', 'posteam_score', 'drive', 'down', 'distance', 'yardline', 'drive_end_yard_line', 'goal_to_go', 'play_type', 'yards_gained', 'first_down', 'passer_id', 'passer_player_name', 'rusher_id', 'rusher_player_name', 'receiver_id', 'receiver_player_name', 'complete_pass', 'sack', 'touchdown', 'drive_result']]
    
    return df

def prep_nfl_data_py_pbp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function takes a Dataframe containing play-by-play data from nfl_data_py,
    performs cleanup operations, and return a cleaned DataFrame for further modeling.

    Parameters:
    <df> (Pandas DataFrame): DataFrame of play-by-play data.

    Returns:
    <df> (Pandas DataFrame): Cleaned DataFrame of play-by-play data.
    """
    df = data_cleanup_nfl_data_py_pbp(df)
    df = filter_subset_pbp_data(nfl_data_py_pbp_df=df)
    
    return df