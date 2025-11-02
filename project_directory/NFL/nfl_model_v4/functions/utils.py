import numpy as np
import pandas as pd

nfl_team_map = {
    'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL', 'Buffalo Bills': 'BUF',
    'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLE',
    'Dallas Cowboys': 'DAL', 'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB',
    'Houston Texans': 'HOU', 'Indianapolis Colts': 'IND', 'Jacksonville Jaguars': 'JAX', 'Kansas City Chiefs': 'KC',
    'Los Angeles Chargers': 'LAC', 'Los Angeles Rams': 'LAR', 'Las Vegas Raiders': 'LV', 'Miami Dolphins': 'MIA',
    'Minnesota Vikings': 'MIN', 'New England Patriots': 'NE', 'New Orleans Saints': 'NO', 'New York Giants': 'NYG',
    'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 'Pittsburgh Steelers': 'PIT', 'San Francisco 49ers': 'SF',
    'Seattle Seahawks': 'SEA', 'Tampa Bay Buccaneers': 'TB', 'Tennessee Titans': 'TEN', 'Washington Commanders': 'WAS'
}

def load_nfl_team_map(nfl_team_map: dict = nfl_team_map) -> dict:
    """
    Function:
    -Load the team map of the "long" version of team names to abbreviations.
    -This map is also used in other functions; this function exists to load 
    from that single source
    
    Parameters:
    <nfl_team_map>: Dictionary with mapping of "long" team names to abbreviations.
    
    Returns:
    <nfl_team_map>: Dictionary with mapping of "long" team names to abbreviations.
    """
    
    return nfl_team_map

def calculate_generic_yardline(df, possession_field, yardline_field):
    def calculate_yardline(row):
        possession_team = row[possession_field]
        yardline_value = row[yardline_field]
        
        if pd.isnull(yardline_value):
            return None
        if possession_team in yardline_value:
            return int(yardline_value.split()[-1])
        else:
            return 100 - int(yardline_value.split()[-1])
    
    if yardline_field == 'drive_end_yard_line':
        df['drive_end_yard_line'] = df.apply(calculate_yardline, axis=1)
        df['drive_end_yard_line'] = df['drive_end_yard_line'].astype('float')        
    else: ## for general cases like drive_start_yard_line
        df['yardline'] = df.apply(calculate_yardline, axis=1)
        df['yardline'] = df['yardline'].astype('float')
    
    return df

def standardize_yard_line(yard_line: str, posteam: str, defteam: str) -> int:
    """
    Function: 
    -Standardize the yard line based on the posteam and defteam.
    1. Handles cases where the yard line is exactly 50. 
    2. processes yard lines like 'ARI 24' or 'WAS 37'.
    
    Parameters:
    <yard_line> (str): The yard line, either as a string (e.g., "ARI 24" or "50").
    <posteam> (str): The team on offense (posteam).
    <defteam> (str): The team on defense (defteam).
    
    Returns:
    (int): The standardized yard line (0-100), where 0 is the defense's goal line and 100 is the posteam's goal line.
    """
    if yard_line == '50' or yard_line == 50:
        return 50
    try:
        if ' ' in yard_line:
            team, yard = yard_line.split()
            yard = int(yard)
            return yard if team == posteam else 100 - yard
        else:
            raise ValueError(f"Yard line '{yard_line}' is improperly formatted or missing a team abbreviation.")
    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}. Yard line: '{yard_line}', Posteam: '{posteam}', Defteam: '{defteam}'")
        return None