import sys
import os
current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.append(parent_dir)

import pandas as pd
from function_library.py_data_engineering.utils import is_empty

def create_quarterback_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function takes a DataFrame containing pbp data from nfl_data_py,
    which includes a 'passer_id' column; this function will apply some logic
    to fill in the 'quarterback_id' for each game based on who threw the most
    recent pass.
    
    Parameters:
    <df> (Pandas DataFrame): DataFrame with columns including ['game_id', 'offense', 'passer_id']
    
    Returns:
    <result_df>: DataFrame with new value, quarterback_id
    """
    def _fill_by_team(group):
        non_empty_mask = group['quarterback_id'].notna() & ~group['quarterback_id'].apply(is_empty)
        valid_ids = group.loc[non_empty_mask, 'quarterback_id'].unique()
        if len(valid_ids) == 0:
            return group
        first_qb = valid_ids[0]
        empty_mask = group['quarterback_id'].isna() | group['quarterback_id'].apply(is_empty)       
        if not empty_mask.any():
            return group
        first_valid_idx = group[non_empty_mask].index[0]
        group.loc[empty_mask & (group.index <= first_valid_idx), 'quarterback_id'] = first_qb
        last_valid_id = None
        for idx in group.index:
            if non_empty_mask.loc[idx]:
                last_valid_id = group.loc[idx, 'quarterback_id']
            elif empty_mask.loc[idx] and last_valid_id is not None:
                group.loc[idx, 'quarterback_id'] = last_valid_id
        return group
    
    df = df.sort_values(by=['game_id','qtr','half_seconds_remaining'], ascending=[True,True,False])
    df['quarterback_id'] = df['passer_id'].astype('object')
    result_df = (df.groupby(['game_id', 'offense'], group_keys=False)
              .apply(_fill_by_team)
              .reset_index(drop=True))
    result_df['quarterback_id'] = result_df['quarterback_id'].apply(
        lambda x: None if is_empty(x) else x
    )
    return result_df

def _create_distance_bucket_column(df: pd.DataFrame, version: str) -> pd.DataFrame:
    """
    Helper Function:
    -Takes a Pandas Dataframe with a "distance" column and buckets those
    distances into groups in a new column, "distance_bucket", which is a "custom" type 
    that sorts logically on its "string" values.
    Note: Used within the create_dn_dst_situational_column function.
    
    Parameters:
    <df> (Pandas Dataframe): DataFrame containing a "distance" column.
    <version> (string): String specifying the "version" of distance cuts to be used. ('v1', 'v2', 'v3')
    <column> (string): String specifying name of the "distance" column if it is not the default value.
    
    Returns:
    <df> (Pandas Dataframe): Updated Dataframe
    """
    if version == 'v1':
        bucket_order = ['1-2', '3-6', '7-9', '10', '11-15', '16+']
        distance_category = pd.CategoricalDtype(categories=bucket_order, ordered=True)
        bins = [0, 2, 6, 9, 10, 15, float('inf')]
        df['distance_bucket'] = pd.cut(df['distance'], bins=bins, labels=bucket_order, right=True)
        df['distance_bucket'] = df['distance_bucket'].astype(distance_category)
    elif version == 'v2':
        bucket_order = ['1', '2', '3', '4-6', '7-9', '10', '11-15', '16+']
        distance_category = pd.CategoricalDtype(categories=bucket_order, ordered=True)
        bins = [0, 1, 2, 3, 6, 9, 10, 15, float('inf')]
        df['distance_bucket'] = pd.cut(df['distance'], bins=bins, labels=bucket_order, right=True)
        df['distance_bucket'] = df['distance_bucket'].astype(distance_category)    
    elif version == 'v3':
        bucket_order = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11-12', '13-15', '16-19', '20+']
        distance_category = pd.CategoricalDtype(categories=bucket_order, ordered=True)
        bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, float('inf')]
        df['distance_bucket'] = pd.cut(df['distance'], bins=bins, labels=bucket_order, right=True)
        df['distance_bucket'] = df['distance_bucket'].astype(distance_category)   
    else:
        raise ValueError("Unknown distance bucketing version entered. Please select a value in ['v1', 'v2', 'v3']")
    return df

def create_dn_dst_situational_column(df: pd.DataFrame, version: str) -> pd.DataFrame:
    """
    Function:
    -Takes a Pandas Dataframe with "down" and "distance" columns and 
    creates a "dn_dst" column that groups situations.

    Parameters:
    <df> (Pandas Dataframe): The input DataFrame.
    <down_col> (str): The name of the column representing "down"; defaults to "down".
    <distance_col> (str): The name of the column representing "distance"; defaults to "distance".

    Returns:
    <df> (Pandas DataFrame): The input DataFrame with a new column 'dn_dst' added.
    """
    df = _create_distance_bucket_column(df, version)
    df['down_string'] = df['down'].apply(lambda x: 'nodown' if pd.isna(x) else str(int(x)))
    df['dn_dst_expanded'] = df['down_string'].astype(str) + "_" + df['distance_bucket'].astype(str)
    if version in ['v1', 'v2']:
        mask = (df['down_string'].isin(['2', '3', '4']) & df['distance_bucket'].isin(['7-9', '10']))
        df.loc[mask, 'dn_dst_expanded'] = df.loc[mask, 'down_string'].astype(str) + "_7-10"
    df.drop(columns=['down_string'], inplace=True)
    return df

def create_ydl_bins(df: pd.DataFrame, bin_type: str) -> pd.DataFrame:
    """
    Function:
    -This function takes a DataFrame containing a 'yardline' column and "bins" those
    yardlines into five yard blocks.
    
    Parameters:
    <df>: DataFrame containing NFL data and a 'yardline' column to be grouped.
    <yardline>: String denoting column name containing yardline to group; defaults to 'yardline'.
    
    Returns:
    <df>: Updated DataFrame with specified yardline_bin_type.
    """
    if bin_type == 'five':
        yard_bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        yard_labels = ["0-5", "6-10", "11-15", "16-20", "21-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", 
                "56-60", "61-65", "66-70", "71-75", "76-80", "81-85", "86-90", "91-95", "96-100"]
        df['yardline_bin_five'] = pd.cut(
            df['yardline'],
            bins=yard_bins,
            labels=yard_labels,
            include_lowest=True
        )
        df['yardline_bin_five'] = df['yardline_bin_five'].astype('category')
    elif bin_type == 'ten':
        yard_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        yard_labels = ["0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"]
        df['yardline_bin_ten'] = pd.cut(
            df['yardline'],
            bins=yard_bins,
            labels=yard_labels,
            include_lowest=True
        )
        df['yardline_bin_ten'] = df['yardline_bin_ten'].astype('category')
    elif bin_type == 'custom_one':
        yard_bin_custom_one = [0, 1, 2, 5, 10, 15, 20, 30, 40, 50, 60, 70, 75, 80, 85, 90, 95, 97, 98, 99]
        yard_labels_custom_one = ["1", "2", "3-5", "5-10", "11-15", "16-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-75", "75-80", "81-85", "86-90", "91-95", "96-97", "98", "99"]
        df['yardline_bin_custom_one'] = pd.cut(
            df['yardline'],
            bins=yard_bin_custom_one,
            labels=yard_labels_custom_one,
            include_lowest=True
        )
        df['yardline_bin_custom_one'] = df['yardline_bin_custom_one'].astype('category')
    else:
        raise ValueError("Unknown Yardline Bucketing Version entered. Please select a value in ['five', 'ten', 'custom_one']")
    return df

def create_score_bin_three_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function takes a DataFrame containing a 'score_differential' column and "bins" by "number" of scores in football jargon.
    
    Parameters:
    <df> (Pandas DataFrame): DataFrame containing NFL data and a 'score_differential' column to be grouped.
    <score_differential>: String denoting column name containing score_differential to group; defaults to 'score_differential'.
    
    Returns:
    <df> (Pandas DataFrame): Updated DataFrame
    """
    score_bins = [ -99, -25, -17, -9, -1, 0, 8, 16, 24, 99]
    score_labels = ["-99 to -25", "-24 to -17", "-16 to -9", "-8 to -1", "0", "1-8", "9-16", "17-24", "25 to 99"]
    df['score_bin_three_scores'] = pd.cut(
                df['score_differential'],
                bins=score_bins,
                labels=score_labels,
                include_lowest=True
            )
    df['score_bin_three_scores'] = df['score_bin_three_scores'].astype('category')
    return df

def create_game_situation_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    - Creates a single categorical column 'game_situation' that incorporates the score differential
    and, for two 5-minute windows in the fourth quarter, the time differential.

    Parameters:
    <df> (Pandas DataFrame): DataFrame containing ['half', 'game_seconds_remaining', 'score_differential'] columns.

    Returns:
    <df> (Pandas Dataframe): NFL play-by-play Dataframe with 'game_situation' column.
    """
    df['game_situation'] = 'other'
    def _apply_game_conditions(df, condition_name, half, time_lower, time_upper):
        game_condition = (
            (df['half'] == half) &
            (df['game_seconds_remaining'] < time_upper) &
            (df['game_seconds_remaining'] >= time_lower)
        )
        conditions = [
            (game_condition & (df['score_differential'] > 24), f'leading_three_plus_scores_{condition_name}'),
            (game_condition & (df['score_differential'] <= 24) & (df['score_differential'] > 16), f'leading_three_scores_{condition_name}'),
            (game_condition & (df['score_differential'] <= 16) & (df['score_differential'] > 8), f'leading_two_scores_{condition_name}'),
            (game_condition & (df['score_differential'] <= 8) & (df['score_differential'] > 0), f'leading_one_score_{condition_name}'),
            (game_condition & (df['score_differential'] == 0), f'tied_{condition_name}'),
            (game_condition & (df['score_differential'] < -8) & (df['score_differential'] >= -16), f'trailing_two_scores_{condition_name}'),
            (game_condition & (df['score_differential'] < -16) & (df['score_differential'] >= -24), f'trailing_three_scores_{condition_name}'),
            (game_condition & (df['score_differential'] < -24), f'trailing_three_plus_scores_{condition_name}')
        ]
        if condition_name not in ('end_of_game','approaching_end_of_game'):
            conditions.append((game_condition & (df['score_differential'] < 0) & (df['score_differential'] >= -8), f'trailing_one_score_{condition_name}'))
        else:
            conditions.append((game_condition & (df['score_differential'] < 0) & (df['score_differential'] >= -3), f'trailing_one_score_fg_range_{condition_name}'))
            conditions.append((game_condition & (df['score_differential'] < -3) & (df['score_differential'] >= -8), f'trailing_one_score_td_range_{condition_name}'))
        for condition, category in conditions:
            df.loc[condition, 'game_situation'] = category
    _apply_game_conditions(df, 'rest_of_game', 1, 1800, 3601)
    _apply_game_conditions(df, 'rest_of_game', 2, 600, 1801)
    _apply_game_conditions(df, 'approaching_end_of_game', 2, 300, 600)
    _apply_game_conditions(df, 'end_of_game', 2, 0, 300)
    _apply_game_conditions(df, 'overtime', 3, 0, 601)
    return df

def create_special_situation_booleans(df: pd.DataFrame, yardline: str='yardline') -> pd.DataFrame:
    """
    Function:
    -This function takes a DataFrame containing ['down', 'distance', 'yardline'] columns and creates several
    special situation Booleans. These mark when the ball is inside the ten, inside the twenty, when it is
    first and five in the open field, and when there is a reduced "landing zone" to acheive a first down
    near the goal line.
    
    Parameters:
    <df> (Pandas DataFrame): DataFrame containing NFL data and a 'yardline' column to be grouped.
    <yardline> (str): String denoting column name containing yardline to group; defaults to 'yardline'.
    
    Returns:
    <df> (Pandas DataFrame): Updated DataFrame
    """
    df['is_inside_ten'] = (df[yardline] >= 90).astype('boolean')
    df['is_inside_twenty'] = ((df[yardline] < 90) & (df[yardline] >= 80)).astype('boolean')
    df['first_five_open_field'] = ((df['goal_to_go']==0) & (df['down']==1) & (df['distance']==5)).astype('boolean')
    df['first_down_landing_zone'] = (100-(df['distance']+df['yardline'])).clip(lower=0, upper=20).astype('category')

    return df

def create_features_nfl_data_py(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -Runs the varius "create_feature" functions for nfl_data_py pbp.
    
    Parameters:
    <df> (Pandas DataFrame): DataFrame with nfl_data_py pbp data.

    Returns:
    <df> (Pandas DataFrame): Updated DataFrame.
    """
    df = create_quarterback_id(df)
    df = create_dn_dst_situational_column(df, version = 'v3')
    df = create_ydl_bins(df, 'five')
    df = create_ydl_bins(df, 'ten')
    df = create_ydl_bins(df, 'custom_one')
    df = create_score_bin_three_scores(df)
    df = create_game_situation_category(df)
    df = create_special_situation_booleans(df)

    return df

