import pandas as pd
from sqlalchemy.exc import IntegrityError
from functions.utils import convert_to_team_abbr, create_nfl_engine

nfl_engine = create_nfl_engine()

def get_game_info_table(bs_obj: object, gm_id: str) -> None:
    """
    Function:
    - Takes a Beautiful Soup object of a PFR game page for specified gm_id,
    pulls out the relevant values, and writes to a MySQL table.

    Parameters:
    <bs_obj> (BS Object): BeautifulSoup object generated from the webpage for the gm_id
    <gm_id> (string): Pro Football Reference game id for a given NFL game

    Returns:
    None
    """
    game_info_dict = {'gmID':gm_id}
    game_info = bs_obj.find('div',{'id':'all_game_info'})
    data_rows = game_info.find_all('tr')

    def _get_text(entry):
        return entry.text.strip()

    for row in data_rows:
        dict_keys = row.find_all('th')
        dict_values = row.find_all('td')

        if dict_keys and dict_values:
            dict_key = _get_text(dict_keys[0])
            dict_value = _get_text(dict_values[0])
            game_info_dict.update({dict_key: dict_value})

    
    game_info_dict['Won Toss'] = game_info_dict.get('Won Toss', '').split(' ')[0].strip()
    try:
        game_info_dict['Toss Decision'] = game_info_dict['Won Toss'].split(' ')[1].strip('()')
    except IndexError:
        game_info_dict['Toss Decision'] = 'Received'

    vegas_line = game_info_dict.get('Vegas Line')
    if vegas_line is not None:
        try:
            game_info_dict['Vegas Favorite'] = vegas_line[:-5].strip()
            game_info_dict['Vegas Line'] = float(vegas_line[-5:])
        except ValueError:
            game_info_dict['Vegas Line'] = 0.0
            game_info_dict['Vegas Favorite'] = 'Pick'
    else:
        game_info_dict['Vegas Line'] = None
        game_info_dict['Vegas Favorite'] = None


    vegas_total = game_info_dict.get('Over/Under')
    if vegas_total is not None:
        game_info_dict['OverUnder'] = float(vegas_total.split(' (')[0])
        game_info_dict.pop('Over/Under')
    else:
        game_info_dict['OverUnder'] = None


    try:
        game_info_dict['Temp_F'] = float(game_info_dict['Weather'].split(' degrees')[0])
        try:
            game_info_dict['Weather'] = game_info_dict['Weather'].split(' degrees, relative humidity ')[1]
            game_info_dict['Humidity_perc'] = float(game_info_dict['Weather'].split('%,')[0])
            if 'no wind' in game_info_dict['Weather']:
                game_info_dict['Wind_mph'] = 0.0
            else:
                game_info_dict['Weather'] =  game_info_dict['Weather'].split('%, wind ')[1]
                game_info_dict['Wind_mph'] = float(game_info_dict['Weather'].split(' mph')[0])
            try:
                game_info_dict['WindChill_F'] = float(game_info_dict['Weather'].split(' mph, wind chill ')[1])
            except IndexError:
                game_info_dict['WindChill_F'] = None
            game_info_dict.pop('Weather')
        except Exception:
            game_info_dict['Humidity_perc'] = None
            game_info_dict['Wind_mph'] = None
            game_info_dict['WindChill_F'] = None
            game_info_dict.pop('Weather')

    except KeyError:
        game_info_dict['Temp_F'] = None
        game_info_dict['Humidity_perc'] = None
        game_info_dict['Weather'] = None
        game_info_dict['Wind_mph'] = None
        game_info_dict['WindChill_F'] = None
        game_info_dict.pop('Weather')


    attendance = game_info_dict.get('Attendance')
    if attendance is not None:
        game_info_dict['Attendance'] = int(attendance.replace(',', ''))
    else:
        game_info_dict['Attendance'] = None

    game_info_dict['Roof'] = game_info_dict.get('Roof', None)
    game_info_dict['Surface'] = game_info_dict.get('Surface', None)

    game_info_dict['Duration'] = game_info_dict.get('Duration', None)

    game_info_dict['Won OT Toss'] = game_info_dict.get('Won OT Toss', None)

    try:
        game_info_dict.pop('Super Bowl MVP')
    except KeyError:
        pass

    game_info_df = pd.DataFrame(game_info_dict, index = [0])

    game_info_df = convert_to_team_abbr(game_info_df, 'Won Toss')
    game_info_df = convert_to_team_abbr(game_info_df, 'Vegas Favorite')
    game_info_df = convert_to_team_abbr(game_info_df, 'Won OT Toss')

    game_info_df.rename(columns={
        'gmID': 'game_id',
        'Won Toss': 'toss_winner',
        'Toss Decision': 'toss_decision',
        'Vegas Line': 'vegas_line',
        'Vegas Favorite': 'vegas_favorite',
        'OverUnder': 'over_under',
        'Temp_F': 'temperature_f',
        'Humidity_perc': 'humidity_percentage',
        'Wind_mph': 'wind_speed_mph',
        'WindChill_F': 'wind_chill_f',
        'Attendance': 'attendance',
        'Roof': 'roof_type',
        'Surface': 'surface_type',
        'Duration': 'game_duration',
        'Won OT Toss': 'ot_toss_winner'
    }, inplace=True)

    table_name = "pfr_game_info"
    try:
        game_info_df.to_sql(table_name, con=nfl_engine, if_exists='append', index=False)
    except IntegrityError as e:
        print(f"Skipping duplicate entries: {e}")

    print(game_info_df)

    return None