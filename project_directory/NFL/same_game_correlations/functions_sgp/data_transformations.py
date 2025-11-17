import numpy as np
import pandas as pd

def build_player_stat_df(schedule_df: pd.DataFrame, player_weekly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function: 
    -Takes a <schedule_df> and <player_weekly_df> containing NFL schedule data and player weekly stat data from nflreadpy; 
    combines the two and returns <player_stat_df>, which adds context from <schedule_df> to <player_weekly_ddf
    
    Parameters:
    <schedule_df> (Pandas DataFrame): DataFrame containing NFL schedule data.
    <player_weekly_df> (Pandas DataFrame): DataFrame containing weekly (game-by-game) NFL player data.

    Returns:
    <player_stat_df> (Pandas DataFrame): Combined DataFrame.
    """
    player_stat_df_away = schedule_df.merge(player_weekly_df, how='right', left_on=['season', 'week', 'away_team'], right_on=['season', 'week', 'team'])
    player_stat_df_away.dropna(subset=['game_id'], inplace=True)
    player_stat_df_home = schedule_df.merge(player_weekly_df, how='left', left_on=['season', 'week', 'home_team'], right_on=['season', 'week', 'team'])
    player_stat_df_home.dropna(subset=['game_id'], inplace=True)
    player_stat_df = pd.concat([player_stat_df_away, player_stat_df_home], axis=0, ignore_index=True)

    conditions = [(player_stat_df['team']==player_stat_df['away_team']), (player_stat_df['team']==player_stat_df['home_team'])]
    choices = [player_stat_df['away_score'], player_stat_df['home_score']]
    player_stat_df['team_pts'] = np.select(conditions, choices, np.nan)
    choices = [player_stat_df['home_score'], player_stat_df['away_score']]
    player_stat_df['opp_pts'] = np.select(conditions, choices, np.nan)
    player_stat_df['team_margin'] = player_stat_df['team_pts'] - player_stat_df['opp_pts']

    return player_stat_df