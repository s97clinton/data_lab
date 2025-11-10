import pandas as pd
import numpy as np

def update_team_abbreviations(df: pd.DataFrame, old_abbv: str, new_abbv: str, game_id_col: str='game_id', offense_col: str='posteam', defense_col: str='defteam') -> pd.DataFrame:
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
    try:
        df[game_id_col] = df[game_id_col].apply(lambda x: x.replace(f'_{old_abbv}_', f'_{new_abbv}_') if old_abbv in x.split('_') else x)
        df[game_id_col] = df[game_id_col].apply(lambda x: x.replace(f'_{old_abbv}', f'_{new_abbv}') if old_abbv in x.split('_') else x)
    except KeyError as e:
        print(f"The {game_id_col} is causing the following exception: {e}")
    try:
        df[offense_col] = df[offense_col].replace(old_abbv, new_abbv)
    except KeyError as e:
        print(f"The {offense_col} is causing the following exception: {e}")
    try:
        df[defense_col] = df[defense_col].replace(old_abbv, new_abbv)
    except KeyError as e:
        print(f"The {defense_col} is causing the following exception: {e}")

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

def calculate_generic_yardline(df: pd.DataFrame, possession_field: str, yardline_field: str) -> pd.DataFrame:
    """
    Function:
    -Takes a <yardline_field> column with the standard 'Team 50' yardline coding and converts
    the value to a 0-100 scale where the "0" and "100" denote the "own endline" and "opponent endline"
    for the team in the <possession_field>.

    Parameters:
    <df> (Pandas DataFrame): DataFrame of NFL pbp_data containing the <possession_field> and <yardline_field>.
    <possession_field> (str): String denoting the column name for the <possession_field>.
    <yardline_field> (str): String denoting the column name for the <yardline_field>.

    Returns:
    <df> (Pandas DataFrame): Updated DataFrame.
    """
    def calculate_yardline(row):
        possession_team = row[possession_field]
        yardline_value = row[yardline_field]
        
        if pd.isnull(yardline_value):
            return None
        if possession_team in yardline_value:
            return int(yardline_value.split()[-1])
        else:
            return 100 - int(yardline_value.split()[-1])
        
    df[yardline_field] = df.apply(calculate_yardline, axis=1).astype('float')
    
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
        "Field goal": "field_goal_made",
        "Missed field goal": "field_goal_miss",
        "Punt": "punt",
        "Turnover on downs": "downs",
        "Safety": "safety",
        "punt_block_safety":"safety",
        "End of half": "end_of_half",
        "fumble": "lost_fumble", 
        "end_of_game": "end_of_half",
        "Opp touchdown": "def_td",
        "int_opp_td": "def_td",
        "int_ret_opp_td": "def_td",
        "lost_fumble_opp_td": "def_td",
        "punt_return_td":"def_td", 
        "punt_returned_opp_td":"def_td", 
        "fga_returned_opp_td":"def_td", 
        "Turnover": "other", 
        "off_fr_td": "other"
    }
    df['drive_result'] = df['drive_result'].replace(drive_result_replacement_dict)

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
    df = calculate_generic_yardline(df, 'posteam', 'drive_start_yard_line')
    df = calculate_generic_yardline(df, 'posteam', 'drive_end_yard_line')
    df = update_column_values(df)
    df = simple_column_creation(df)
    df = parse_weather_column(df)    
    return df

def filter_and_subset_nfl_data_py_pbp(pbp_df = pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -Applies a 'play_type' filter and subsets relevant columns for final pbp training set.

    Parameters:
    <pbp_df> (Pandas DataFrame): DataFrame of play-by-play data.

    Returns:
    <df> (Pandas DataFrame): Cleaned DataFrame of play-by-play data.
    """
    df = pbp_df.copy()
    df = df[df['play_type'].isin(['run', 'pass', 'qb_kneel', 'qb_spike'])]
    df = df[['game_id', 'season', 'week', 'stadium', 'roof', 'temp', 'wind', 'offense', 'defense', 'home_team_on_offense', 'half', 'qtr', 'game_seconds_remaining', 'half_seconds_remaining', 'score_differential', 'posteam_score', 'drive', 'down', 'distance', 'yardline', 'drive_end_yard_line', 'goal_to_go', 'play_type', 'yards_gained', 'first_down', 'passer_id', 'passer_player_name', 'rusher_id', 'rusher_player_name', 'receiver_id', 'receiver_player_name', 'complete_pass', 'sack', 'touchdown', 'drive_result']]
    return df

def drive_time_processing_steps(df: pd.DataFrame, column: str = 'drive_game_clock_start') -> pd.DataFrame:
    """
    Function:
    -This function will take a Pandas Dataframe and use the columns in the table to convert a time 
    string to a continuous value denoting the seconds remaining in the half. <df> must
    contain (1) a "time" column to convert and (2) a "qtr" columns to give context to how much time
    is left in the half.
    
    Parameters:
    <df>: Pandas Dataframe with the time field for conversion ["drive_game_clock_start"]
    
    Returns:
    <update_df>: Pandas Dataframe with the time field converted
    """
    def _preprocess_drive_start_time(time_str: str) -> str:
        """
        Function:
        -Helper Function to preprocess the <time_str> value in a specified column;
        this function will remove any leading "00:" from the time string to ensure
        it is in MM:SS format.
        """
        if pd.isna(time_str) or time_str is None:
            return None
        if time_str.startswith("00:") and len(time_str) == 8:
            time_str = time_str[3:]
        return time_str
    def _convert_to_seconds(quarter: int, time_str: str) -> int:
        """
        Function:
        -Helper Function to use the (1) quarter and (2) time column to process the <time_str>
        value in a specified column into seconds; the value returned will be the seconds
        remaining in the half of an NFL football game.
        """
        if pd.isna(time_str) or time_str is None:
            return None
        
        try:
            minutes, seconds = map(int, time_str.split(':'))
        except ValueError:
            return None
        
        total_seconds = minutes * 60 + seconds
        if quarter in [1.0, 3.0]:
            return (15 * 60) + total_seconds
        elif quarter in [2.0, 4.0, 5.0]:
            return total_seconds
    
    update_df = df.copy()
    update_df['temp_drive_start_time'] = update_df[column].apply(_preprocess_drive_start_time)    
    update_df['half_seconds_remaining'] = update_df.apply(lambda row: _convert_to_seconds(row['qtr'], row['temp_drive_start_time']), axis=1)
    update_df.drop(columns=['temp_drive_start_time'], inplace=True)
    
    return update_df

def nfl_data_py_pbp_to_drives(pbp_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function takes a pandas dataframe, <df>, from the MongoDB collection nfl_data_py_pbp_data,
    and rolls that play-by-play data up to the drive level.
    
    Parameters:
    <pbp_df> (Pandas Dataframe): Dataframe with nfl_data_py pbp data. 
    
    Returns:
    <drive_df> (Pandas Dataframe): Dataframe with "drive level" data.
    """
    df = pbp_df[['season', 'game_id', 'start_time', 'stadium', 'roof', 'surface', 'temp', 'wind', 'home_team', 'away_team', 'season_type', 'week', 'offense', 'defense', 'home_team_on_offense', 'score_differential', 'half', 'qtr', 'drive', 'drive_quarter_start', 'drive_quarter_end', 'drive_game_clock_start', 'drive_game_clock_end','drive_time_of_possession', 'drive_start_yard_line', 'drive_end_yard_line', 'drive_play_id_started', 'drive_play_id_ended', 'drive_play_count', 'drive_first_downs', 'fixed_drive_result', 'drive_result', 'extra_point_attempt', 'extra_point_result', 'two_point_attempt', 'two_point_conv_result', 'kickoff_attempt', 'rush_attempt', 'pass_attempt', 'field_goal_attempt', 'punt_attempt', 'penalty_dead_ball_no_play', 'penalty_unknown_no_play', 'penalty_live_snap_no_play', 'aborted_play', 'qb_dropback', 'qb_kneel', 'qb_spike', 'qb_scramble', 'qb_hit', 'complete_pass', 'incomplete_pass', 'sack', 'solo_tackle', 'assist_tackle', 'tackled_for_loss', 'fumble_forced', 'fumble_not_forced', 'fumble_out_of_bounds']]
    group_by_cols = ['game_id', 'drive']
    static_cols = ['season', 'start_time', 'stadium', 'roof', 'surface', 'temp', 'wind', 'home_team', 'away_team', 'season_type', 'week', 'offense', 'defense', 'home_team_on_offense', 'score_differential', 'half', 'qtr', 'drive_quarter_start', 'drive_quarter_end', 'drive_game_clock_start', 'drive_game_clock_end', 'drive_time_of_possession', 'drive_start_yard_line', 'drive_end_yard_line', 'drive_play_id_started', 'drive_play_id_ended', 'drive_play_count', 'drive_first_downs', 'fixed_drive_result', 'drive_result', 'extra_point_attempt','extra_point_result', 'two_point_attempt','two_point_conv_result']
    sum_cols = ['kickoff_attempt', 'rush_attempt', 'pass_attempt', 'field_goal_attempt', 'punt_attempt', 'penalty_dead_ball_no_play', 'penalty_unknown_no_play','penalty_live_snap_no_play', 'aborted_play', 'qb_dropback', 'qb_kneel', 'qb_spike', 'qb_scramble', 'qb_hit', 'complete_pass', 'incomplete_pass', 'sack', 'solo_tackle', 'assist_tackle', 'tackled_for_loss', 'fumble_forced', 'fumble_not_forced', 'fumble_out_of_bounds']

    drive_df = df.groupby(group_by_cols).agg({**{col: 'last' for col in static_cols}, **{col: 'sum' for col in sum_cols}}).reset_index()
    drive_df = drive_time_processing_steps(drive_df)
    drive_df['total_penalties'] = drive_df['penalty_dead_ball_no_play'] + drive_df['penalty_unknown_no_play'] + drive_df['penalty_live_snap_no_play'] 
    drive_df.rename(columns={'rush_attempt': 'rush_attempts', 'pass_attempt': 'pass_dropbacks','sack': 'sacks'}, inplace=True)
    drive_df['counted_penalties'] = drive_df['drive_play_count'] - drive_df['rush_attempts'] - drive_df['pass_dropbacks']

    return drive_df

def filter_and_subset_nfl_drive_df(drive_df = pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -Filters the drive_df and subsets relevant columns for final drive training set.

    Parameters:
    <drive_df> (Pandas DataFrame): DataFrame of play-by-play data.

    Returns:
    <df> (Pandas DataFrame): Cleaned DataFrame of play-by-play data.
    """
    df = drive_df.copy()
    df = df[~(df['drive_result']=='other')]
    df = df[['game_id', 'drive', 'season', 'week', 'offense', 'defense', 'home_team_on_offense', 'score_differential', 'half', 'qtr', 'half_seconds_remaining', 'drive_start_yard_line', 'drive_end_yard_line', 'drive_result', 'drive_play_count', 'rush_attempts', 'pass_dropbacks', 'sacks', 'counted_penalties', 'total_penalties']]
    
    return df

def nfl_data_py_weekly_transform_import(df: pd.DataFrame) -> pd.DataFrame:
    """
    Helper Function:
    -This function takes a DataFrame containing imported data from nfl_data_py_weekly and performs 
    cleanup steps.
    
    Parameters:
    <df> (Pandas DataFrame): Pandas DataFrame containing data from nfl_data_py_weekly
    
    Returns:
    <df (Pandas DataFrame): Updated DataFrame.
    """
    df.rename(columns={'recent_team': 'offense', 'opponent_team': 'defense'}, inplace=True)
    df = df[df['offense'] != df['defense']].copy()
    df[['offense', 'defense']] = df[['offense', 'defense']].replace('LA', 'LAR')
    df.loc[df['player_name'] == 'Taysom Hill', ['position', 'position_group']] = 'TE'
    df['yards_per_rec'] = df['receiving_yards'] / df['receptions']
    df['yards_per_rec'] = df['yards_per_rec'].fillna(0)
    df['tgt_conv_rate'] = df['receptions'] / df['targets']
    df['tgt_conv_rate'] = df['tgt_conv_rate'].fillna(0)
    df['target_share'] = df['target_share'].fillna(0)
    df = df.sort_values(by=['season', 'week', 'offense'])
    df['team_total_carries'] = df.groupby(['offense', 'season', 'week'])['carries'].transform('sum')
    df['team_total_rushing_tds'] = df.groupby(['offense', 'season', 'week'])['rushing_tds'].transform('sum')  
    df['team_total_receiving_tds'] = df.groupby(['offense', 'season', 'week'])['receiving_tds'].transform('sum')
    df['carry_share'] = df.apply(lambda row: row['carries'] / row['team_total_carries'] if row['team_total_carries'] > 0 else 0, axis=1)
    df['rush_td_share'] = df.apply(lambda row: row['rushing_tds'] / row['team_total_rushing_tds'] if row['team_total_rushing_tds'] > 0 else 0, axis=1)
    df['rec_td_share'] = df.apply(lambda row: row['receiving_tds'] / row['team_total_receiving_tds'] if row['team_total_receiving_tds'] > 0 else 0, axis=1)
    
    return df

def prep_schedule_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -Prepare imported schedule data from nfl_data_py for use; the 'weather' columns in the
    schedule data are inconsistent, and were dropped in favor of 'weather' data available
    via the pbp_data, which can be accessed as necessary.

    Parameters:
    <df> (Pandas DataFrame): DataFrame containing NFL schedule data.

    Returns:
    <df> (Pandas DataFrame): Updated DataFrame
    """
    df[['away_team', 'home_team']] = df[['away_team', 'home_team']].replace('LA', 'LAR')
    df['neutral_site'] = df['location'] == 'Neutral'
    df.drop(columns=['location'], inplace=True)
    df.rename(columns={'spread_line':'away_spread'}, inplace=True)
    df['home_spread'] = df['away_spread'] * (-1)
    home_spread_conditions = [df['home_spread'] > (df['away_score'] - df['home_score']), df['home_spread'] == (df['away_score'] - df['home_score'])]
    home_spread_choices = ['win', 'push']
    df['home_spread_result'] = np.select(home_spread_conditions, home_spread_choices, default='loss')
    total_conditions = [df['total_line'] < df['total'], df['total_line'] == df['total']]
    total_conditions_choices = ['over', 'push']
    df['total_result'] = np.select(total_conditions, total_conditions_choices, default='under')
    df = df[['season', 'week', 'game_id', 'gameday', 'gametime', 'game_type', 'neutral_site', 'stadium_id', 'stadium', 'away_team', 'home_team', 
             'away_rest', 'home_rest', 'away_moneyline', 'home_moneyline', 'away_spread', 'home_spread', 'away_spread_odds', 'home_spread_odds',
             'total_line', 'under_odds', 'over_odds', 'div_game', 'roof',
             'away_coach', 'home_coach', 'referee',
             'away_qb_id', 'home_qb_id', 'away_qb_name', 'home_qb_name',
             'away_score', 'home_score', 'result', 'total', 'overtime',
             'home_spread_result', 'total_result']]
    
    return df

def convert_schedule_to_test_frame(df: pd.DataFrame, test_split_season: int, test_split_week: int) -> pd.DataFrame:
    """
    Function:
    -Takes a 'prepared' <df> of NFL schedule data, splits into two copies to establish test sets for both
    the home and away team on the schedule to project offense vs. defense, then concatenates the
    two DataFrames to form and return <full_test_df>. The <test_split_week> denotes the final week that will
    be included in TRAINING set (i.e. (<test_split_season > == 2025) & (<test_split_week> > 9) would make
    2025, weeks 10 and forward, the TEST set).

    Parameters:
    <df> (Pandas DataFrame): 'Prepared' NFL schedule DataFrame.
    <test_split_season> (int): Integer denoting the season to "split" into test set.
    <test_week_season> (int): Integer denoting the week to "split"; all future weeks will be in test set.

    Returns:
    <full_test_df> (Pandas DataFrame): DataFrame with all offense/defense matchups for games to project.
    """
    test_df = df[(df['season'] == test_split_season) & (df['week'] > test_split_week)].copy()
    test_df = test_df[['season', 'week', 'game_id', 'gameday', 'gametime', 'neutral_site', 'away_team', 'away_coach', 'away_qb_name', 'away_qb_id', 'home_team', 'home_coach', 'home_qb_name', 'home_qb_id']]
    away_test_df = test_df.copy()
    away_test_df.drop(columns=['home_qb_name', 'home_qb_id'], inplace=True)
    away_test_df.rename(columns={'away_team': 'offense', 'away_coach': 'offense_coach', 'away_qb_name': 'offense_qb_name', 'away_qb_id': 'offense_qb_id', 'home_team': 'defense', 'home_coach': 'defense_coach'}, inplace=True)
    away_test_df['home_team_on_offense'] = False
    home_test_df = test_df.copy()
    home_test_df.drop(columns=['away_qb_name', 'away_qb_id'], inplace=True)
    home_test_df.rename(columns={'home_team': 'offense', 'home_coach': 'offense_coach', 'home_qb_name': 'offense_qb_name', 'home_qb_id': 'offense_qb_id', 'away_team': 'defense', 'away_coach': 'defense_coach'}, inplace=True)
    home_test_df['home_team_on_offense'] = True
    full_test_df = pd.concat([away_test_df, home_test_df], ignore_index=True)
    full_test_df = full_test_df.sort_values(by=['season', 'week', 'gameday', 'gametime', 'game_id'])
    
    return full_test_df
        
def convert_test_output_to_game_outcomes(test_output: pd.DataFrame, train_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -Convert drive-level projections to game-level projections.

    Parameters:
    <test_output> (DataFrame): DataFrame containing drive-level projections.

    Returns:
    <game_projections> (DataFrame): DataFrame containing game-level projections.
    """
    df = test_output.copy()
    df['proj_pts_per_drive'] = (df['prob_field_goal_made']*3) + (df['prob_off_kor_td']*7) + (df['prob_pass_td']*7) + (df['prob_rush_td']*7)
    df['opp_def_proj_pts_per_drive'] = (df['prob_safety']*2) + (df['prob_def_td']*7)
    drives_per_gm_train_set = (
        train_df.groupby(['game_id', 'offense'])
        .size()
        .groupby('offense')
        .agg(
            mean_drives = ('mean'),
            median_drives = ('median'),
            std_drives = ('std'),
            games_played = ('count')
        )
        .reset_index()
    )
    df = df.merge(drives_per_gm_train_set, on = 'offense', how = 'left')
    game_projection_df = df[df['home_team_on_offense']].copy()
    game_projection_df = game_projection_df[['season', 'week', 'game_id', 'gameday', 'gametime', 'neutral_site']]
    home_score_df = df[df['home_team_on_offense']].copy()
    home_score_df.rename(columns={'offense':'home', 'offense_coach':'home_coach', 'offense_qb_name':'home_qb_name', 'offense_qb_id':'home_qb_id', 
                                  'proj_pts_per_drive':'home_proj_pts_per_drive', 'opp_def_proj_pts_per_drive':'away_def_proj_pts_per_drive', 'mean_drives':'home_mean_drives'}, inplace=True)
    home_score_df = home_score_df[['game_id', 'home', 'home_coach', 'home_qb_name', 'home_qb_id', 'home_proj_pts_per_drive', 'away_def_proj_pts_per_drive', 'home_mean_drives']]
    away_score_df = df[~(df['home_team_on_offense'])].copy()
    away_score_df.rename(columns={'offense':'away', 'offense_coach':'away_coach', 'offense_qb_name':'away_qb_name', 'offense_qb_id':'away_qb_id', 
                                  'proj_pts_per_drive':'away_proj_pts_per_drive', 'opp_def_proj_pts_per_drive':'home_def_proj_pts_per_drive', 'mean_drives':'away_mean_drives'}, inplace=True)
    away_score_df = away_score_df[['game_id', 'away', 'away_coach', 'away_qb_name', 'away_qb_id', 'away_proj_pts_per_drive', 'home_def_proj_pts_per_drive', 'away_mean_drives']]
    game_projection_df = game_projection_df.merge(home_score_df, how="inner", on="game_id")
    game_projection_df = game_projection_df.merge(away_score_df, how="inner", on="game_id")
    game_projection_df['proj_drives'] = (game_projection_df['home_mean_drives'] + game_projection_df['away_mean_drives'])/2
    game_projection_df['away_proj_pts'] = round(game_projection_df['proj_drives'] * (game_projection_df['away_proj_pts_per_drive'] + game_projection_df['away_def_proj_pts_per_drive']), 2)
    game_projection_df['home_proj_pts'] = round(game_projection_df['proj_drives'] * (game_projection_df['home_proj_pts_per_drive'] + game_projection_df['home_def_proj_pts_per_drive']), 2)
    game_projection_df['spread'] = round(game_projection_df['away_proj_pts'] - game_projection_df['home_proj_pts'], 2)
    game_projection_df['total'] = round(game_projection_df['away_proj_pts'] + game_projection_df['home_proj_pts'], 2)

    game_projection_df = game_projection_df[['season', 'week', 'game_id', 'gameday', 'gametime', 'neutral_site', 
                                             'away', 'away_coach', 'away_qb_name', 'home', 'home_coach', 'home_qb_name',
                                             'away_proj_pts', 'home_proj_pts', 'spread', 'total']]

    return game_projection_df