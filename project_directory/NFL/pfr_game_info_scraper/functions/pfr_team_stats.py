import pandas as pd
from sqlalchemy.exc import IntegrityError
from functions.utils import convert_to_team_abbr, create_nfl_engine

nfl_engine = create_nfl_engine()

def _get_team_stats_basics_parse_html(bs_obj: object) -> list:
    """
    Helper Function:
    -This function takes a BeautifulSoup object from a Pro Football Reference Game Page
    and parses it to pull out the "team_stats_basics" table.

    Parameters:
    <bs_obj> (BS Object): BeautifulSoup object from a Pro Football Reference Game Page.

    Returns:
    <team_stats_basics> (list): A list of two lists containing scoring data by quarter for the teams.
    """
    try:
        base_scoring_table = bs_obj.find('table', {'class':'linescore nohover stats_table no_freeze'})
        data_rows = base_scoring_table.find('tbody').find_all('tr')
        team_stats_basics = []
        for row in data_rows:
            rows = row.find_all('td')
            rows = [score.text.strip() for score in rows]
            rows.pop(0)
            if len(rows) == 6:
                rows.insert(-1,None)
            if len(rows) == 8:
                rows.pop(-3)
            team_stats_basics.append(rows)
    except AttributeError as e:
        print(f"No base scoring table, {e}")
    return team_stats_basics

def _team_stats_basics_df(team_stat_basics: list, gm_id: str, year: int, week: int) -> tuple:
    """
    Helper Function:
    -This Helper Function will take the list of lists in team_stat_basics and
    will convert it to a Pandas Dataframe. It will then tag the data with new
    header columns and some general game information passed in by the other parameter.

    Parameters:
    <team_stat_basics> (list): A list of two lists containing scoring data by quarter for the respective teams.
    <gm_id> (string): Pro Football Reference game id for a given NFL game.
    <year> (int): The NFL season of targeted games to scrape.
    <week> (int): The NFL week of targeted games to scrape.

    Returns:
    <team_stats_basics_df> (Pandas DF): A Pandas Dataframe containing the team_stat_basics data
    <teams> (list): A list containing abbreviations of the two teams that participated in the game.
    """
    team_stats_basics_df = pd.DataFrame(team_stat_basics)
    team_stats_basics_df.columns = ['team','q1','q2','q3','q4','ot','final']
    team_stats_basics_df = convert_to_team_abbr(team_stats_basics_df, 'team')
    opponents = [team_stats_basics_df['team'][1],team_stats_basics_df['team'][0]]
    team_stats_basics_df['opp'] = opponents
    venue = ['Away','Home']
    team_stats_basics_df['venue'] = venue
    team_stats_basics_df['game_id'] = gm_id
    team_stats_basics_df['season'] = year
    team_stats_basics_df['week'] = week
    team_stats_basics_df['key'] = team_stats_basics_df['team'] + team_stats_basics_df['game_id']

    teams = [team_stats_basics_df['team'][0],team_stats_basics_df['team'][1]]

    return team_stats_basics_df, teams

def get_team_stats_basics(bs_obj: object, gm_id: str, year: int, week: int) -> list:
    """
    Function:
    -Get the basic team stat table from the BeautifulSoup object, 
    write the data to a MySQL table, and return a list with two
    items in it, the (1) away and (2) home team from the NFL game.

    Parameters:
    <bs_obj> (BS Object): BeautifulSoup object containing PFR Game Info.
    <gm_id> (string): Pro Football Reference game id for a given NFL game.
    <year> (int): The NFL season of targeted games to scrape.
    <week> (int): The NFL week of targeted games to scrape.

    Returns:
    <teams> (list): A list with two items, the (1) away and (2) home team.
    """
    team_stats_basics = _get_team_stats_basics_parse_html(bs_obj)
    team_stats_basics_df, teams = _team_stats_basics_df(team_stats_basics, gm_id, year, week)
    
    table_name = "pfr_game_basic"
    try:
        team_stats_basics_df.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
    except IntegrityError as e:
        print(f"Skipping duplicate entries: {e}")

    return teams


def _get_team_stats_full_parse_html(bs_obj: object) -> tuple:
    """
    Helper Function:
    -This function takes a BeautifulSoup object from a Pro Football Reference Game Page
    and parses it to pull out the "team_stats_full" table.

    Parameters:
    <bs_obj> (BS Object): BeautifulSoup object from a Pro Football Reference Game Page.

    Returns:
    <headers> (list): A list of headers for the team stats table.
    <data> (list): A list of lists containing the team stats data.
    """
    try:
        team_stats = bs_obj.find('table',{'id':'team_stats'})
        headers = team_stats.find('thead').find('tr').find_all('th')
        headers = [header.text.strip() for header in headers]
        headers.pop(0)
        headers.insert(0,'Team')
        data_rows = team_stats.find('tbody').find_all('tr')
        data = []
        for row in data_rows:
            rows = row.find_all('td')
            rows = [stat.text.strip() for stat in rows]
            statName = row.find('th')
            statName = statName.text.strip()
            rows.insert(0,statName)
            data.append(rows)
    except AttributeError as e:
        print(f"No Team Statistics, {e}")
    return headers, data

def __split_and_assign(df: pd.DataFrame, col_name: str, new_cols: list, sep: str='-') -> None:
    """
    Utility Function:
    -Splits a pandas dataframe column and expands; if there is a 
    value error, replaces values with zeroes.
    """
    try:
        df[new_cols] = df[col_name].str.split(sep, expand=True)
    except ValueError:
        df[new_cols] = [0,0,0]

def _process_team_stats(df: pd.DataFrame, gm_id: str) -> pd.DataFrame:
    """
    Helper Function:
    -Takes the data in team_stats_full dataframe, breaks up certain fields into
    component parts, and returns a transformed dataframe.

    Parameters:
    <df> (Pandas Dataframe): Pandas Dataframe with PFR team_stats_full.
    <gm_id> (string): Pro Football Reference game id for a given NFL game.

    Returns:
    <df> (Pandas Dataframe): Transformed version of Pandas Dataframe with PFR team_stats_full.
    """
    df = df.set_index('Team').T
    team_list = df.index.tolist()
    df['Team'] = team_list
    df = convert_to_team_abbr(df, 'Team')
    df['firstDowns'] = df['First Downs']
    __split_and_assign(df, 'Rush-Yds-TDs', ['rushAtt','rushYds','rushTD'])
    __split_and_assign(df, 'Cmp-Att-Yd-TD-INT', ['passCom','passAtt','passYds','passTD','thrownINT'])
    __split_and_assign(df, 'Sacked-Yards', ['sacked','sackedYDS'])
    df['netPassYds'] = df['Net Pass Yards']
    df['totalYds'] = df['Total Yards']
    __split_and_assign(df, 'Fumbles-Lost', ['fumbles','fumblesLost'])
    df['turnovers'] = df['Turnovers']
    __split_and_assign(df, 'Penalties-Yards', ['pen','penYds'])
    __split_and_assign(df, 'Third Down Conv.', ['thirdDnConv','thirdDnAtt'])
    __split_and_assign(df, 'Fourth Down Conv.', ['fourthDnConv','fourthDnAtt'])
    df['possessionTime'] = df['Time of Possession']
    df = df.drop(['First Downs','Rush-Yds-TDs','Cmp-Att-Yd-TD-INT','Sacked-Yards','Net Pass Yards','Total Yards','Fumbles-Lost','Turnovers','Penalties-Yards','Third Down Conv.','Fourth Down Conv.','Time of Possession'],axis=1)
    df['gmID'] = gm_id
    df['key'] = df['Team'] + df['gmID']
    df.reset_index(drop=True,inplace=True)
    df.rename_axis("",axis="columns",inplace=True)
    df.rename(columns={'gmID':'game_id',
                       'Team':'team',
                       'firstDowns':'first_downs',
                       'rushAtt':'rush_attempts',
                       'rushYds':'rush_yards',
                       'rushTD':'rush_touchdowns',
                       'passCom':'pass_completions',
                       'passAtt':'pass_attempts',
                       'passYds':'pass_yards',
                       'passTD':'pass_touchdowns',
                       'thrownINT':'offense_interceptions',
                       'sacked':'sacked',
                       'sackedYDS':'sacked_yards',
                       'netPassYds':'net_pass_yards',
                       'totalYds':'total_yards',
                       'fumbles':'fumbles',
                       'fumblesLost':'fumbles_lost',
                       'turnovers':'turnovers',
                       'pen':'penalties',
                       'penYds':'penalty_yards',
                       'thirdDnConv':'third_down_conversions',
                       'thirdDnAtt':'third_down_attempts',
                       'fourthDnConv':'fourth_down_conversions',
                       'fourthDnAtt':'fourth_down_attempts',
                       'possessionTime':'time_of_possession'}, inplace=True)

    return df



def get_team_stats_full(bs_obj: object, gm_id: str) -> None:
    """
    Function:
    -Get the full team stat table from the BeautifulSoup object and 
    write the data to a MySQL table.

    Parameters:
    <bs_obj> (BS Object): BeautifulSoup object containing PFR Game Info.
    <gm_id> (string): Pro Football Reference game id for a given NFL game.

    Returns:
    None
    """
    headers, data = _get_team_stats_full_parse_html(bs_obj)
    try:
        team_stats_full_df = pd.DataFrame(data, columns = headers)
    except ValueError as e:
        print(f"Issue with team stats, {e}")
    team_stats_full_df = _process_team_stats(team_stats_full_df, gm_id)

    table_name = 'pfr_team_stats'
    try:
        team_stats_full_df.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
    except IntegrityError as e:
        print(f"Skipping duplicate entries: {e}")

    print(team_stats_full_df)



def extract_drive_table(bs_obj: object, gm_id: str, teams: list, year: int, week: int, possession: str) -> pd.DataFrame:
    """
    Function
    - Given the beautiful soup object containing the targeted table, the 
    string containing the game ID, and a list of the road and home teams,
    return Pandas Dataframe of the table. It also has a possession parameter
    that expects either home or away to set variables further on.

    Parameters:
    <bs_obj> (BS Object): BeautifulSoup object containing PFR Game Info.
    <gm_id> (string): Pro Football Reference game id for a given NFL game.
    <teams> (list): A list containing the two teams that played in the game.
    <year> (int): The NFL season of targeted games to scrape.
    <week> (int): The NFL week of targeted games to scrape.
    <possession> (string): A string that is either 'home' or 'away' to indicate which team is on offense.

    Returns:
    <data> (Pandas DataFrame): A Pandas DataFrame containing the drive information
    extracted from the BeautifulSoup object.   
    """
    data_rows = bs_obj.find('tbody').find_all('tr')
    data = []
    for row in data_rows:
        rows = row.find_all('td')
        rows = [stat.text.strip() for stat in rows]
        breakdown = row.find_all('span',{'class':'tooltip'})
        breakdown = str(breakdown).split('"')[3]
        drivePasses = int(str(breakdown).split(', ')[0][:-4].rstrip())
        driveRushes = int(str(breakdown).split(', ')[1][:-4].rstrip())
        drivePenalties = int(str(breakdown).split(', ')[2][:-7].rstrip())
        if (drivePasses+driveRushes+drivePenalties) == 0:
            drivePasses = None
            driveRushes = None
            drivePenalties = None
        elif (drivePasses+driveRushes+drivePenalties) == rows[3]:
            print('The number of plays in the drive are not adding up.')
        else:
            pass
        if possession == 'home':
            rows.insert(1,teams[0])
            rows.insert(2,teams[1])
            rows.insert(3,'home')
        elif possession == 'away':
            rows.insert(1,teams[1])
            rows.insert(2,teams[0])
            rows.insert(3,'away')
        rows.insert(4,week)
        rows.insert(4,year)
        rows.insert(9,drivePenalties)
        rows.insert(9,driveRushes)
        rows.insert(9,drivePasses)
        data.append(rows)
    headers = ['qtr','def','off','venue','season','week',
               'drive_start_time','drive_start_ydl','drive_plays',
               'drive_passes','drive_runs','drive_penalties','drive_time','drive_net_yds','drive_result']
    try:
        data = pd.DataFrame(data, columns = headers)
    except AttributeError as e:
        print(f"The drive frame columns are off, {e}.")
        
    data['key'] = data['season'].astype(str) + data['week'].astype(str) + '_' + data['qtr'].astype(str) + '_' + data.index.astype(str) + data['off'] + data['def']
    
    return data

def get_drive_info(bs_obj: object, gm_id: str, teams: list, year: int, week: int) -> None:
    """
    Function:
    -Takes a beautiful soup object of a PFR game page
    and writes the Drive Info to a MySQL table, appending the teams, year, and week.

    Parameters:
    <bs_obj> (BS Object): BeautifulSoup object containing PFR Game Info.
    <gm_id> (string): Pro Football Reference game id for a given NFL game.
    <teams> (list): A list containing the two teams that played in the game.
    <year> (int): The NFL season of targeted games to scrape.
    <week> (int): The NFL week of targeted games to scrape.

    Returns:
    None: This function writes the drive information to a MySQL table.
    """
    try:
        home_drives = bs_obj.find('table',{'id':'home_drives'})
        home_drives = extract_drive_table(home_drives,gm_id,teams,year,week,'home')
        table_name = 'pfr_drive_info'
        try:
            home_drives.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
        except IntegrityError as e:
            print(f"Skipping duplicate entries: {e}")
        
        print(home_drives)
    except AttributeError as e:
        print(f"No Home Drive Info, {e}")

    try:
        away_drives = bs_obj.find('table',{'id':'vis_drives'})
        away_drives = extract_drive_table(away_drives,gm_id,teams,year,week,'away')
        table_name = 'pfr_drive_info'
        try:
            away_drives.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
        except IntegrityError as e:
            print(f"Skipping duplicate entries: {e}")

        print(away_drives)
    except AttributeError as e:
        print(f"No Away Drive Info, {e}")
