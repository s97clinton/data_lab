import pandas as pd
from sqlalchemy import create_engine
from functions.credentials import MYSQL_USER, MYSQL_PASSWORD

def create_nfl_engine(user: str = MYSQL_USER, password: str = MYSQL_PASSWORD, host: str = 'localhost', port: int = 3306, database: str = 'nfl') -> object:
    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)

    return engine

def convert_to_team_abbr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Function:
    -This function will take a Pandas Dataframe with "alternate" NFL team names
    (long form, etc.) and maps the names to the standard "abbreviation".
    
    Note: At present, the team map is written within this function; if it is
    ever needed elsewhere, this should be moved upstream.

    Parameters:
    <df> (pd.DataFrame): Pandas DataFrame containing the column to modify.
    <column> (str): Name of the column to update.

    Returns:
    <df> (pd.DataFrame): Pandas DataFrame with updated values in specified column.
    """
    team_map = {
        'ARZ': 'ARI', 'Cardinals': 'ARI', 'Arizona Cardinals': 'ARI',
        'Falcons': 'ATL', 'Atlanta Falcons': 'ATL',
        'Ravens': 'BAL', 'Baltimore Ravens': 'BAL',
        'Bills': 'BUF', 'Buffalo Bills': 'BUF',
        'Panthers': 'CAR', 'Carolina Panthers': 'CAR',
        'Bears': 'CHI', 'Chicago Bears': 'CHI',
        'Bengals': 'CIN', 'Cincinnati Bengals': 'CIN',
        'Browns': 'CLE', 'Cleveland Browns': 'CLE',
        'Cowboys': 'DAL', 'Dallas Cowboys': 'DAL',
        'Broncos': 'DEN', 'Denver Broncos': 'DEN',
        'Lions': 'DET', 'Detroit Lions': 'DET',
        'GNB': 'GB', 'Packers': 'GB', 'Green Bay Packers': 'GB',
        'Texans': 'HOU', 'Houston Texans': 'HOU',
        'Colts': 'IND', 'Indianapolis Colts': 'IND',
        'Jaguars': 'JAX', 'Jacksonville Jaguars': 'JAX',
        'KAN': 'KC', 'Chiefs': 'KC', 'Kansas City Chiefs': 'KC',
        'SD': 'LAC', 'SDG': 'LAC', 'Chargers': 'LAC', 'Los Angeles Chargers': 'LAC', 'San Diego Chargers': 'LAC',
        'STL': 'LAR', 'Rams': 'LAR', 'Los Angeles Rams': 'LAR', 'St. Louis Rams': 'LAR',
        'Dolphins': 'MIA', 'Miami Dolphins': 'MIA',
        'Vikings': 'MIN', 'Minnesota Vikings': 'MIN',
        'NWE': 'NE', 'Patriots': 'NE', 'New England Patriots': 'NE',
        'NOR': 'NO', 'Saints': 'NO', 'New Orleans Saints': 'NO',
        'Giants': 'NYG', 'New York Giants': 'NYG',
        'Jets': 'NYJ', 'New York Jets': 'NYJ',
        'OAK': 'LVR', 'Raiders': 'LVR', 'Oakland Raiders': 'LVR', 'Los Angeles Raiders': 'LVR', 'Las Vegas Raiders': 'LVR',
        'Eagles': 'PHI', 'Philadelphia Eagles': 'PHI',
        'Steelers': 'PIT', 'Pittsburgh Steelers': 'PIT',
        'SFO': 'SF', '49ers': 'SF', 'San Francisco 49ers': 'SF',
        'Seahawks': 'SEA', 'Seattle Seahawks': 'SEA',
        'TAM': 'TB', 'Buccaneers': 'TB', 'Tampa Bay Buccaneers': 'TB',
        'Titans': 'TEN', 'Tennessee Titans': 'TEN', 'Oilers': 'TEN', 'Houston Oilers': 'TEN',
        'WAS': 'WSH', 'Redskins': 'WSH', 'Washington Redskins': 'WSH',
        'Washington Football Team': 'WSH', 'Washington Commanders': 'WSH'
    }

    df[column] = df[column].replace(team_map)

    return df

def extract_pfr_row_data(bs_obj: object) -> list:
    """
    Function:
    -Extracts the data out of the rows in a Pro Football Reference
    Table.

    Parameters:
    <bs_obj> (BS Object): Beautiful Soup object containing pbp row data.

    Returns:
    <data> (List): List of lists containing the data from the table.
    """
    data = []
    for row in bs_obj:
        rows = row.find_all('td')
        rows = [stat.text.strip() for stat in rows]
        data.append(rows)
        
    return data



