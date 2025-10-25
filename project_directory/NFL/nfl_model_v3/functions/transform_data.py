import pandas as pd

def merge_ratings(base_df, rating_df, base_df_type):
    """
    Function:
    -Merges team ratings with the training dataframes
    for each side of the ball and returns the original dataframe
    with the supplemented information.

    Parameters:
    <base_df> (Pandas Dataframe): The base df with teams by season, offense, and 
    defense to merge off_rating and def_rating by season for each side of the ball.
    <rating_df> (Pandas Dataframe): The dataframe with the ratings to merge.
    <base_df_type> (string): String value that merges differently based on different
    "base_df" values; allowed values are "drive_df" and "player_stat_df", else the 
    function returns a ValueError.

    Returns:
    <base_df> (Pandas Dataframe): The original Dataframe supplemented with offensive
    and defensive ratings.
    """
    if base_df_type == 'drive_df':
        base_df = base_df.merge(rating_df[['team', 'season', 'off_rating']], 
                                        left_on=['off', 'season'], 
                                        right_on=['team', 'season'],
                                        how='left')
        base_df = base_df.drop('team', axis=1)

        base_df = base_df.merge(rating_df[['team', 'season', 'def_rating']], 
                                        left_on=['def', 'season'], 
                                        right_on=['team', 'season'],
                                        how='left')
        base_df = base_df.drop('team', axis=1)

    elif base_df_type == 'player_stat_df':

        base_df = base_df.merge(rating_df[['team', 'season', 'off_rating']], 
                                        left_on=['Tm', 'season'], 
                                        right_on=['team', 'season'],
                                        how='left')
        base_df = base_df.drop('team', axis=1)

        base_df = base_df.merge(rating_df[['team', 'season', 'def_rating']], 
                                        left_on=['Opp', 'season'], 
                                        right_on=['team', 'season'],
                                        how='left')
        base_df = base_df.drop('team', axis=1)

    else:
        raise ValueError(f"Unsupported value: {base_df_type}. Expected value of 'drive_df' or 'player_stat_df'")

    return base_df

def merge_off_coach_qb(base_df, coach_qb_df):
    """
    Function:
    -This function is set up to merge the <drive_train_df> produced in the
    run_nfl_model_data_import function with the <coach_qb_df> for offensive info,
    but it could be easily adapted to merge the coach_qb_df for defensive coaches
    or to attach to another dataframe.

    Parameters:
    <base_df> (Pandas Dataframe): The base df with teams by season, week, and offense
    to merge.
    <coach_qb_df> (Pandas Dataframe): The dataframe with the coach and starting qb info to merge.

    Returns:
    <base_df> (Pandas Dataframe): The dataframe supplemented with the coach/qb info.
    """
    base_df = base_df.merge(coach_qb_df[['season', 'week', 'team', 'designer_offense',
                                         'playcaller_offense','primary_qb','backup_qb']], 
                                    left_on=['off', 'season', 'week'], 
                                    right_on=['team', 'season', 'week'],
                                    how='left')
    base_df = base_df.drop('team', axis=1)

    return base_df

def prep_nfl_model_data(current_rating_df, hist_rating_df, coach_qb_df, pfr_rush_df, pfr_rec_df, pfr_drive_df, current_season, current_week):
    """
    Function: 
    -This function takes the various dataframes imported in the nfl_model_v3 process
    and transforms the data so it is ready for use in modeling.

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

    rush_df = merge_ratings(pfr_rush_df, rating_df, base_df_type="player_stat_df")
    rush_df = rush_df[(rush_df['season']<current_season)|((rush_df['season']==current_season) * (rush_df['week'] < current_week))]

    rec_df = merge_ratings(pfr_rec_df, rating_df, base_df_type="player_stat_df")
    rec_df = rec_df[(rec_df['season']<current_season)|((rec_df['season']==current_season) * (rec_df['week'] < current_week))]

    drive_df = merge_ratings(pfr_drive_df, rating_df, base_df_type="drive_df")
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


def prep_drive_test_frames(nfl_schedule,current_rating,current_week):
    """
    Function:
    -Creates the test frames for the home and away variations
    of offense/defense for the NFL games on selected portion of
    the schedule and attaches the appropriate team ratings for the
    current week.

    Parameters:
    <nfl_schedule> (Pandas Dataframe): Dataframe with NFL schedule
    <current_rating> (Pandas Dataframe): Dataframe with current NFL team ratings

    Returns:
    <> (Pandas Dataframe): Dataframe ready to pass in as test data to 
    drive_result model.
    """
    proj_df = nfl_schedule[(nfl_schedule['week']==current_week)]
    drive_test_df_away = proj_df[['season','week','away','home']]
    drive_test_df_away = drive_test_df_away.rename(columns={'away':'off','home':'def'})
    drive_test_df_away['venue'] = 'away'
    drive_test_df_away = merge_ratings(drive_test_df_away, current_rating, base_df_type="drive_df")

    drive_test_df_home = proj_df[['season','week','home','away']]
    drive_test_df_home = drive_test_df_home.rename(columns={'home':'off','away':'def'})
    drive_test_df_home['venue'] = 'home'
    drive_test_df_home = merge_ratings(drive_test_df_home, current_rating, base_df_type="drive_df")

    drive_test_df = pd.concat([drive_test_df_away,drive_test_df_home], ignore_index=True)

    return drive_test_df

