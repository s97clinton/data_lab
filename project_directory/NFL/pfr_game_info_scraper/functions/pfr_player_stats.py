import pandas as pd
from sqlalchemy.exc import IntegrityError
from functions.utils import convert_to_team_abbr, create_nfl_engine

nfl_engine = create_nfl_engine()

def _extract_pfr_player_rows(bs_obj: object, gm_id: str) -> list:
    """
    Helper Function:
    -Takes a BeautifulSoup object and extracts the player stats, takes
    the gm_id as an extra parameter for tagging purposes.

    Parameters:
    <bs_obj> (BS Object): BeautifulSoup object containing PFR Game Info.
    <gm_id> (string): Pro Football Reference game id for a given NFL game.

    Returns:
    <data> (list): List of lists containing the data in the PFR player table.
    """
    data = []
    for row in bs_obj:
        rows = row.find_all('td')
        rows = [stat.text.strip() for stat in rows]
        name = row.find('th')
        player_name = name.text.strip()
        if 'Player' in player_name:
            continue
        if player_name == '':
            continue
        try:
            name_link = str(name)
            name_link = name_link.split('><a href="/players/')[1]
            name_link = name_link.split('.htm')[0]
        except Exception:
            name_link = name.text.strip()
        rows.insert(0,gm_id)
        rows.insert(0,player_name)
        rows.insert(0,name_link)
        data.append(rows)

    return data

def _extract_pfr_player_stat_table(bs_obj: object, gm_id: str) -> pd.DataFrame:
    """
    Helper Function:
    -Takes a BeautifulSoup object containing a player stats table
    and converts that table to a Pandas Dataframe.

    Parameters:
    <bs_obj> (BS Object): BeautifulSoup object containing PFR Game Info.
    <gm_id> (string): Pro Football Reference game id for a given NFL game.

    Returns:
    <data> (list): List of lists containing the data in the PFR player table.
    """
    headers = bs_obj.find('tr',{'class':'thead'}).find_all('th')
    headers = [header.text.strip() for header in headers]
    headers.insert(1,'gmID')
    headers.insert(0,'playerID')

    data_rows = bs_obj.find('tbody').find_all('tr')
    data = _extract_pfr_player_rows(data_rows, gm_id)

    try:
        data = pd.DataFrame(data, columns = headers)
    except ValueError as e:
        if 'Passing' and 'Rushing' and 'Receiving' in headers:
            headers = ['playerID','Player','gmID','Tm','Cmp','PassAtt','PassYds','PassTD','INT','Sk','SkYds','CmpLng','PassRate','RushAtt','RushYds','RushTD','RushLng','Tgt','Rec','RecYds','RecTD','RecLng','Fmb','FmbLost']
            try:
                data = pd.DataFrame(data, columns = headers)
            except ValueError as e:
                print(f"{e}, problem with Pass/Rush/Receive reroute")
            data.loc[data['PassAtt']=='','PassAtt'] = 0
            data.loc[data['RushAtt']=='','RushAtt'] = 0
            data.loc[data['Tgt']=='','Tgt'] = 0
        
        elif 'Def Interceptions' and 'Tackles' and 'Fumbles' in headers:
            headers = ['playerID','Player','gmID','Tm','Int','IntYds','IntTD','IntLng','PassD','Sk','TotalTkl','SoloTkl','AsstTkl','TFL','QBHit','FR','FRyds','FRTD','FF']
            try:
                data = pd.DataFrame(data, columns = headers)
            except ValueError as e:
                print(f"{e}, problem with the Basic Player Defense reroute")
        
        else:
            print(f"Unknown Headers, {e}")
            pass

    data['key'] = data['playerID'] + data['gmID']
    data = convert_to_team_abbr(data, 'Tm')

    return data

class get_player_stats:

    @staticmethod
    def get_passing_info(bs_obj: object, gm_id: str) -> None:
        """
        Function:
        -Takes a BeautifulSoup object containing a player stats table,
        extracts the passing info, and writes that to a MySQL DB.

        Parameters:
        <bs_obj> (BS Object): BeautifulSoup object containing PFR Game Info.
        <gm_id> (string): Pro Football Reference game id for a given NFL game.

        Returns:
        None: Writes to DB
        """
        try:
            pass_rush_run_data =  bs_obj.find('table',{'id':'player_offense'})
            pass_rush_run_data = _extract_pfr_player_stat_table(pass_rush_run_data, gm_id)
            pass_df = pass_rush_run_data[pass_rush_run_data['PassAtt'].astype(int) > 0]
            pass_df = pass_df[['playerID','Player','gmID','Tm','Cmp','PassAtt','PassYds','PassTD','INT','Sk','SkYds','CmpLng','PassRate','Fmb','FmbLost','key']]
            pass_df.rename(columns={'playerID':'player_id',
                                    'Player':'player_name',
                                    'gmID':'game_id',
                                    'Tm':'team',
                                    'Cmp':'completions',
                                    'PassAtt':'pass_attempts', 
                                    'PassYds':'passing_yards',
                                    'PassTD':'passing_touchdowns',
                                    'INT':'interceptions',
                                    'Sk':'sacks',
                                    'SkYds':'sack_yards',
                                    'CmpLng':'longest_completion',
                                    'PassRate':'passer_rating',
                                    'Fmb':'fumbles',
                                    'FmbLost':'fumbles_lost'}, inplace=True)
            table_name = "pfr_passing_base"
            try:
                pass_df.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
            except IntegrityError as e:
                print(f"Skipping duplicate entries: {e}")

            print(pass_df)
        except AttributeError as e:
            raise AttributeError('No Basic Offense Stats for Players') from e
        
        try:
            advanced_passing =  bs_obj.find('table',{'id':'passing_advanced'})
            advanced_passing = _extract_pfr_player_stat_table(advanced_passing, gm_id)
            advanced_passing = advanced_passing.drop(['Cmp','Att','Yds','Sk','Prss','Prss%'], axis=1)
            advanced_passing['1D'] = advanced_passing['1D'].replace('',0)
            advanced_passing['1D%'] = advanced_passing['1D%'].replace('',0.0)
            advanced_passing['CAY/Cmp'] = advanced_passing['CAY/Cmp'].replace('',0.0)
            advanced_passing['YAC/Cmp'] = advanced_passing['YAC/Cmp'].replace('',0.0)
            advanced_passing.rename(columns={'playerID':'player_id',
                                             'Player':'player_name',
                                             'gmID':'game_id',
                                             'Tm':'team',
                                             '1D':'first_downs',
                                             '1D%':'first_down_percentage',
                                             'IAY':'incomplete_air_yards',
                                             'IAY/PA':'incomplete_air_yards_per_attempt',
                                             'CAY':'completed_air_yards',
                                             'CAY/Cmp':'completed_air_yards_per_completion',
                                             'CAY/PA':'completed_air_yards_per_attempt',
                                             'YAC':'yards_after_catch',
                                             'YAC/Cmp':'yards_after_catch_per_completion',
                                             'Drops':'drops',
                                             'Drop%':'drop_percentage',
                                             'BadTh':'bad_throws',
                                             'Bad%':'bad_throws_percentage',
                                             'Bltz':'blitzes_faced',
                                             'Hrry':'times_hurried',
                                             'Hits':'times_hits',
                                             'Scrm':'scrambles',
                                             'Yds/Scr':'yards_per_scramble'}, inplace=True)

            table_name = "pfr_passing_adv"
            try:
                advanced_passing.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
            except IntegrityError as e:
                print(f"Skipping duplicate entries: {e}")

            print(advanced_passing)

        except AttributeError as e:
            raise AttributeError('No Advanced Passing for Players') from e

    @staticmethod
    def get_rushing_info(bs_obj: object, gm_id: str) -> None:
        """
        Function:
        -Takes a BeautifulSoup object containing a player stats table,
        extracts the rushing info, and writes that to a MySQL DB.

        Parameters:
        <bs_obj> (BS Object): BeautifulSoup object containing PFR Game Info.
        <gm_id> (string): Pro Football Reference game id for a given NFL game.

        Returns:
        None: Writes to DB
        """
        try:
            pass_rush_run_data =  bs_obj.find('table',{'id':'player_offense'})
            pass_rush_run_data = _extract_pfr_player_stat_table(pass_rush_run_data, gm_id)
            rush_df = pass_rush_run_data[pass_rush_run_data['RushAtt'].astype(int) > 0]
            rush_df = rush_df[['playerID','Player','gmID','Tm','RushAtt','RushYds','RushLng','RushTD','Fmb','FmbLost','key']]
            rush_df.rename(columns={'playerID':'player_id',
                                   'Player':'player_name',
                                   'gmID':'game_id',
                                   'Tm':'team',
                                   'RushAtt':'rush_attempts', 
                                   'RushYds':'rushing_yards',
                                   'RushLng':'longest_rush',
                                   'RushTD':'rushing_touchdowns',
                                   'Fmb':'fumbles',
                                   'FmbLost':'fumbles_lost'}, inplace=True)
            table_name = "pfr_rushing_base"
            try:
                rush_df.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
            except IntegrityError as e:
                print(f"Skipping duplicate entries: {e}")

            print(rush_df)
        except AttributeError as e:
            raise AttributeError('No Basic Offense Stats for Players') from e
        try:
            advanced_rushing =  bs_obj.find('table',{'id':'rushing_advanced'})
            advanced_rushing = _extract_pfr_player_stat_table(advanced_rushing, gm_id)
            advanced_rushing = advanced_rushing.drop(['Att','Yds','TD'], axis=1)
            advanced_rushing.rename(columns={'playerID':'player_id',
                                             'Player':'player_name',
                                             'gmID':'game_id',
                                             'Tm':'team',
                                             '1D':'first_downs',
                                             'YAC':'yards_after_contact',
                                             'YAC/Att':'yards_after_contact_per_attempt',
                                             'YBC':'yards_before_contact',
                                             'YBC/Att':'yards_before_contact_per_attempt',
                                             'BrkTkl':'broken_tackles',
                                             'Att/Br':'attempts_per_broken_tackle',
                                             'Lng':'longest_rush'}, inplace=True)

            table_name = "pfr_rushing_adv"
            try:
                advanced_rushing.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
            except IntegrityError as e:
                print(f"Skipping duplicate entries: {e}")

            print(advanced_rushing)

        except AttributeError as e:
            raise AttributeError('No Advanced Rushing for Players') from e

    @staticmethod
    def get_receiving_info(bs_obj: object, gm_id: str) -> None:
        """
        Function:
        -Takes a BeautifulSoup object containing a player stats table,
        extracts the receiving info, and writes that to a MySQL DB.

        Parameters:
        <bs_obj> (BS Object): BeautifulSoup object containing PFR Game Info.
        <gm_id> (string): Pro Football Reference game id for a given NFL game.

        Returns:
        None: Writes to DB
        """
        try:
            pass_rush_run_data =  bs_obj.find('table',{'id':'player_offense'})
            pass_rush_run_data = _extract_pfr_player_stat_table(pass_rush_run_data, gm_id)
            rec_df = pass_rush_run_data[pass_rush_run_data['Tgt'].astype(int) > 0]
            rec_df = rec_df[['playerID','Player','gmID','Tm','Tgt','Rec','RecYds','RecTD','RecLng','Fmb','FmbLost','key']]
            rec_df.rename(columns={'playerID':'player_id',
                                  'Player':'player_name',
                                  'gmID':'game_id',
                                  'Tm':'team',
                                  'Tgt':'targets', 
                                  'Rec':'receptions',
                                  'RecYds':'receiving_yards',
                                  'RecTD':'receiving_touchdowns',
                                  'RecLng':'longest_reception',
                                  'Fmb':'fumbles',
                                  'FmbLost':'fumbles_lost'}, inplace=True)
            table_name = "pfr_receiving_base"
            try:
                rec_df.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
            except IntegrityError as e:
                print(f"Skipping duplicate entries: {e}")

            print(rec_df)
        except AttributeError as e:
            raise AttributeError('No Basic Offense Stats for Players') from e
        try:
            advanced_receiving =  bs_obj.find('table',{'id':'receiving_advanced'})
            advanced_receiving = _extract_pfr_player_stat_table(advanced_receiving, gm_id)
            advanced_receiving = advanced_receiving.drop(['Tgt','Rec','Yds','TD','Int','Rat'], axis=1)
            advanced_receiving.rename(columns={'playerID':'player_id',
                                             'Player':'player_name',
                                             'gmID':'game_id',
                                             'Tm':'team',
                                             '1D':'first_downs',
                                             'YAC':'yards_after_catch',
                                             'YAC/R':'yards_after_catch_per_reception',
                                             'YBC':'yards_before_catch',
                                             'YBC/R':'yards_before_catch_per_reception',
                                             'ADOT':'average_depth_of_target',
                                             'BrkTkl':'broken_tackles',
                                             'Rec/Br':'receptions_per_broken_tackle',
                                             'Drop':'drops',
                                             'Drop%':'drop_percentage'}, inplace=True)

            table_name = "pfr_receiving_adv"
            try:
                advanced_receiving.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
            except IntegrityError as e:
                print(f"Skipping duplicate entries: {e}")

            print(advanced_receiving)

        except AttributeError as e:
            raise AttributeError('No Advanced Receiving for Players') from e

