import pandas as pd
from functions.utils import extract_pfr_row_data

def _extract_pfr_pbp(bs_pbp_table: object, teams: list, year: int, week: int) -> None:
    """
    Helper Function:
    -Takes the Beautiful Soup object containing the targeted play-by-play table and the 
    string containing the game ID, return Pandas Dataframe of the play-by-play table.

    Parameters:
    <bs_pbp_table> (BS Object): BeautifulSoup object containing play-by-play table.
    <teams> (list): List of the two teams in NFL Game, (1) away and (2) home.
    <year> (int): The NFL season of targeted games to scrape.
    <week> (int): The NFL week of targeted games to scrape.

    Returns:
    None: Exports a .csv file to directory and prints the DataFrame to verify the code ran.
    """
    headers = bs_pbp_table.find('thead').find_all('th')
    headers = [header.text.strip() for header in headers]
    headers.pop(0)
    print(headers)

    data_rows = bs_pbp_table.find('tbody').find_all('tr')
    data = extract_pfr_row_data(data_rows)
    for row in data:
        if len(row) == 1:
            data.remove(row)
        else:
            pass
    
    try:
        pbp_df = pd.DataFrame(data, columns = headers)
    except ValueError as e:
        print(f"Header Issue, {e}")

    pbp_df['QB'] = ""
    pbp_df['PlayType'] = ""
    pbp_df['WR'] = ""
    pbp_df['Route'] = ""
    pbp_df['FZ'] = ""
    pbp_df['PassRes'] = ""
    pbp_df['ThrowGrade'] = ""
    pbp_df['Comment'] = ""

    current_columns = pbp_df.columns.tolist()
    fixed_columns_1 = ['Time', 'Down', 'ToGo', 'Location', 'EPB', 'EPA']
    fixed_columns_2 = ['QB', 'PlayType', 'WR', 'Route', 'FZ', 'PassRes', 'ThrowGrade', 'Comment', 'Detail']
    fixed_columns = fixed_columns_1 + fixed_columns_2
    dynamic_team_columns = [col for col in current_columns if col not in fixed_columns]

    final_column_order = fixed_columns_1 + dynamic_team_columns + fixed_columns_2
    pbp_df = pbp_df[final_column_order]

    print(pbp_df)
    pbp_df.to_csv('/Users/stevenjclinton/Documents/Scuba Steve Football/NFL Game Film Notes/'+str(year)+'/'+str(week)+'/'+teams[0]+teams[1]+'.csv')


def get_pbp(bs_obj: object, teams: list, year: int, week: int) -> None:
    """
    Function:
    -Extracts the play-by-play from the BeautifulSoup object
    and exports to .csv file in "Game Film" Directory.

    Parameters:
    <bs_obj> (BS Object): BeautifulSoup object containing PFR Game Info.
    <teams> (list): List of the two teams in NFL Game, (1) away and (2) home.
    <year> (int): The NFL season of targeted games to scrape.
    <week> (int): The NFL week of targeted games to scrape.

    Returns:
    None: Exports a .csv file to directory.
    """

    try:
        bs_pbp_table = bs_obj.find('table',{'id':'pbp'})
        _extract_pfr_pbp(bs_pbp_table, teams, year, week)
    except AttributeError as e:
        raise AttributeError('No Play by Play') from e