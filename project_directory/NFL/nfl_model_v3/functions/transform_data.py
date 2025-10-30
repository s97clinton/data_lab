import pandas as pd
from typing import Tuple

def merge_ratings(train_df: pd.DataFrame, rating_df: pd.DataFrame, train_df_type: str) -> pd.DataFrame:
    """
    Function:
    -Takes <train_df> (<train_df_type> options: drive_df or player_stat_df) and merges team ratings
    for each side of the ball; returns the merged DataFrame.

    Parameters:
    <train_df> (Pandas Dataframe): The base df with teams by season, offense, and 
    defense to merge off_rating and def_rating by season for each side of the ball.
    <rating_df> (Pandas Dataframe): The dataframe with the ratings to merge.
    <train_df_type> (string): String value that merges differently based on different
    "train_df" values; allowed values are "drive_df" and "player_stat_df", else the 
    function returns a ValueError.

    Returns:
    <df> (Pandas Dataframe): Updated DataFrame.
    """
    df = train_df.copy()
    updated_rating_df = rating_df.copy()
    updated_rating_df['team'] = updated_rating_df['team'].replace({'LV': 'LVR', 'WAS': 'WSH'})
    if train_df_type == 'drive_df':
        df = df.merge(updated_rating_df[['team', 'season', 'off_rating']], 
                                        left_on=['off', 'season'], 
                                        right_on=['team', 'season'],
                                        how='left')
        df = df.drop('team', axis=1)

        df = df.merge(updated_rating_df[['team', 'season', 'def_rating']], 
                                        left_on=['def', 'season'], 
                                        right_on=['team', 'season'],
                                        how='left')
        df = df.drop('team', axis=1)

    elif train_df_type == 'player_stat_df':

        df = df.merge(updated_rating_df[['team', 'season', 'off_rating']], 
                                        left_on=['team', 'season'], 
                                        right_on=['team', 'season'],
                                        how='left')
        df = df.drop('team', axis=1)

        df = df.merge(updated_rating_df[['team', 'season', 'def_rating']], 
                                        left_on=['opp', 'season'], 
                                        right_on=['team', 'season'],
                                        how='left')
        df = df.drop('team', axis=1)

    else:
        raise ValueError(f"Unsupported value: {train_df_type}. Expected value of 'drive_df' or 'player_stat_df'")

    return df

def merge_off_coach_qb(train_df: pd.DataFrame, coach_qb_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function:
    -This function is set up to merge the <drive_train_df> produced in the
    run_nfl_model_data_import function with the <coach_qb_df> for offensive info;
    it could easily be adapted to merge the coach_qb_df for defensive coaches
    or to attach to another dataframe.

    Parameters:
    <train_df> (Pandas Dataframe): The base df with teams by season, week, and offense
    to merge.
    <coach_qb_df> (Pandas Dataframe): The dataframe with the coach and starting qb info to merge.

    Returns:
    <df> (Pandas Dataframe): The dataframe supplemented with the coach/qb info.
    """
    df = train_df.copy()
    df = df.merge(coach_qb_df[['season', 'week', 'team', 'designer_offense',
                                         'playcaller_offense','primary_qb','backup_qb']], 
                                    left_on=['off', 'season', 'week'], 
                                    right_on=['team', 'season', 'week'],
                                    how='left')
    df = df.drop('team', axis=1)

    return df

def prep_nfl_model_data(current_rating_df: pd.DataFrame, 
                        hist_rating_df: pd.DataFrame, 
                        coach_qb_df: pd.DataFrame, 
                        pfr_rush_df: pd.DataFrame, 
                        pfr_rec_df: pd.DataFrame, 
                        pfr_drive_df: pd.DataFrame, 
                        current_season: int, 
                        current_week: int) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Function: 
    -This function takes the specified dataframes (imported in the nfl_model_v3 process)
    and transforms the data so it is ready for use in modeling; it returns three dataframes:
    rush_df, rec_df, and drive_df.

    Parameters:
    <hist_rating_df> (Pandas Dataframe): Pandas Dataframe w/ hist_rating_df data
    <coach_qb_df> (Pandas Dataframe): Pandas Dataframe w/ coach_qb_df data
    <pfr_game_basic> (Pandas Dataframe): Pandas Dataframe w/ pfr_game_basic data
    <pfr_rush_df> (Pandas Dataframe): Pandas Dataframe w/ pfr_rush_df data
    <pfr_rec_df> (Pandas Dataframe): Pandas Dataframe w/ pfr_rec_df data
    <pfr_drive_df> (Pandas Dataframe): Pandas Dataframe w/ pfr_drive_df data

    Returns:
    <rush_df> (Pandas Dataframe): Pandas Dataframe w/ rushing data for modeling
    <rec_df> (Pandas Dataframe): Pandas Dataframe w/ receiving data for modeling
    <drive_df> (Pandas Dataframe): Pandas Dataframe w/ drive data for modeling
    """
    rating_df = pd.concat([hist_rating_df, current_rating_df], ignore_index=True)

    rush_df = merge_ratings(pfr_rush_df, rating_df, train_df_type="player_stat_df")
    rush_df = rush_df[(rush_df['season']<current_season)|((rush_df['season']==current_season) * (rush_df['week'] < current_week))]

    rec_df = merge_ratings(pfr_rec_df, rating_df, train_df_type="player_stat_df")
    rec_df = rec_df[(rec_df['season']<current_season)|((rec_df['season']==current_season) * (rec_df['week'] < current_week))]

    drive_df = merge_ratings(pfr_drive_df, rating_df, train_df_type="drive_df")
    drive_df = merge_off_coach_qb(drive_df, coach_qb_df)
    drive_df = drive_df.rename(columns={'drivePlays':'total_plays','drivePasses':'pass_att','driveRuns':'rush_att','drivePenalties':'total_penalties','driveTime': 'drive_time','driveResult': 'drive_result'})
    drive_results_updated = {
        'Blocked FG':'fg_fail',
        'Blocked FG, Downs':'fg_fail',
        'Blocked Punt':'punt',
        'Blocked Punt, Downs':'punt',
        'Downs':'downs',
        'End of Game':'end_of_game',
        'End of Half':'end_of_half',
        'Field Goal':'fg_made',
        'Fumble':'fumble',
        'Fumble, Safety':'safety',
        'Interception':'interception',
        'Missed FG':'fg_fail',
        'Punt':'punt',
        'Safety':'safety',
        'Touchdown':'touchdown'
    }
    drive_df['drive_result'] = drive_df['drive_result'].replace(drive_results_updated)

    drive_df = drive_df[['season','week','off','def','venue','off_rating','def_rating','drive_result']]
    drive_df = drive_df[(drive_df['season']<current_season)|((drive_df['season']==current_season) * (drive_df['week'] < current_week))]

    return rush_df, rec_df, drive_df


def prep_drive_test_frames(nfl_schedule: pd.DataFrame, current_rating: pd.DataFrame, current_week: int) -> pd.DataFrame:
    """
    Function:
    -Creates the test frames for the home and away variations
    of offense/defense for the NFL games on selected portion of
    the schedule and attaches the appropriate team ratings for the
    current week; returns Dataframe ready to pass in as test data to 
    drive_result model

    Parameters:
    <nfl_schedule> (Pandas Dataframe): Dataframe with NFL schedule
    <current_rating> (Pandas Dataframe): Dataframe with current NFL team ratings
    <current_week> (int): Current week of the NFL season to create test frames for

    Returns:
    <drive_test_df> (Pandas Dataframe): Dataframe ready to pass in as test data to drive_result model.
    """
    proj_df = nfl_schedule[(nfl_schedule['week']==current_week)]
    drive_test_df_away = proj_df[['season','week','away','home']]
    drive_test_df_away = drive_test_df_away.rename(columns={'away':'off','home':'def'})
    drive_test_df_away['venue'] = 'away'
    drive_test_df_away = merge_ratings(drive_test_df_away, current_rating, train_df_type="drive_df")

    drive_test_df_home = proj_df[['season','week','home','away']]
    drive_test_df_home = drive_test_df_home.rename(columns={'home':'off','away':'def'})
    drive_test_df_home['venue'] = 'home'
    drive_test_df_home = merge_ratings(drive_test_df_home, current_rating, train_df_type="drive_df")

    drive_test_df = pd.concat([drive_test_df_away,drive_test_df_home], ignore_index=True)

    return drive_test_df

def convert_drive_results_to_drive_points(model_output_df: pd.DataFrame, drive_count_df: pd.DataFrame, nfl_schedule: pd.DataFrame, current_season: int, current_week: int) -> pd.DataFrame:
    """
    Function:
    -Transform output of multinomial logistic regression model into 
    NFL spread and total by converting the fg and td outputs; returns an updated DataFrame
    with points per drive for each offense.

    Parameters:
    <model_output_df> (Pandas Dataframe): Dataframe with output of projections
    from multinomial logistic regression model to transform into points per drive
    for each offense in NFL game
    <drive_count_df> (Pandas Dataframe): Dataframe with average drives per game by offense
    <nfl_schedule> (Pandas Dataframe): Dataframe with schedule data for the current projection week
    <current_season> (int): Current NFL season for filtering drive counts

    Returns:
    <matchup_df> (Pandas Dataframe): Dataframe with projected game outputs.
    """
    df = model_output_df.copy()
    df['points_per_drive'] = (df['fg_made']*3) + (df['touchdown']*7)
    df = df[['season','week','off','def','venue','points_per_drive']]
    current_drive_count_df = drive_count_df.copy()
    current_drive_count_df = current_drive_count_df[current_drive_count_df['season'] == current_season]
    df = df.merge(current_drive_count_df[['off','avg_drives_per_game']], left_on=['off'], right_on=['off'], how='left')
    proj_df = nfl_schedule[(nfl_schedule['week']==current_week)]
    matchup_df = proj_df.merge(df, left_on=['season','week','away'], right_on=['season','week','off'], how='left')
    matchup_df = matchup_df.rename(columns={'points_per_drive':'away_points_per_drive','avg_drives_per_game':'away_avg_drives_per_game'})
    matchup_df = matchup_df.merge(df, left_on=['season','week','home'], right_on=['season','week','off'], how='left')
    matchup_df = matchup_df.rename(columns={'points_per_drive':'home_points_per_drive','avg_drives_per_game':'home_avg_drives_per_game'})
    matchup_df['projected_drives'] = (matchup_df['away_avg_drives_per_game'] + matchup_df['home_avg_drives_per_game']) / 2
    matchup_df['away_projected_points'] = round(matchup_df['away_points_per_drive'] * matchup_df['projected_drives'], 2)
    matchup_df['home_projected_points'] = round(matchup_df['home_points_per_drive'] * matchup_df['projected_drives'], 2)
    matchup_df['projected_spread'] = round(matchup_df['away_projected_points'] - matchup_df['home_projected_points'], 2)
    matchup_df['projected_total'] = round(matchup_df['home_projected_points'] + matchup_df['away_projected_points'], 2)
    matchup_df = matchup_df[['season','week','away','home','away_projected_points','home_projected_points', 'projected_spread','projected_total']]

    return matchup_df
