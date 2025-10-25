import cloudscraper
from bs4 import BeautifulSoup
import time

from functions.pfr_game_info_table import get_game_info_table
from functions.pfr_team_stats import get_team_stats_basics, get_team_stats_full, get_drive_info
from functions.pfr_player_stats import get_player_stats
from functions.pfr_pbp_gamesheet import get_pbp

def scrape_pfr_game_pages(game_ids: list, year: int, week: int, all_stats: bool = False, scrape_pbp: bool = False) -> None:
    """
    Function:
    - Takes a list of Pro Football Reference Game IDs and scrapes data for those games.
    - Uses year and week parameters to designate the NFL season/week.
    - Option to acquire full stats or just the boxscore via all_stats parameter.
    - Option to scrape play-by-play data via scrape_pbp parameter.
    
    Parameters:
    <game_ids> (list of strings): A list containing the PFR game IDs for the requested subset.
    <year> (int): The NFL season of targeted games to scrape.
    <week> (int): The NFL week of targeted games to scrape.
    <all_stats> (bool): Whether to acquire full statistics or just the boxscore.
    <scrape_pbp> (bool): Whether to scrape play-by-play data.

    Returns:
    None: Writes output to a MySQL database and .csv files.
    """
    scraper = cloudscraper.create_scraper()
    for gm_id in game_ids:
        url = f'https://www.pro-football-reference.com/boxscores/{gm_id}.htm'
        try:
            response = scraper.get(url)
            print(f"Scraping {gm_id} - Status Code: {response.status_code}")
            if response.status_code != 200:
                print(f"Failed to retrieve page for game {gm_id}: {response.status_code} - {response.reason}")
                continue
            html = response.text.replace("<!--", "").replace("-->", "")
            bs_obj = BeautifulSoup(html, 'html.parser')
            get_game_info_table(bs_obj, gm_id)
            teams = get_team_stats_basics(bs_obj, gm_id, year, week)
            if all_stats:
                get_team_stats_full(bs_obj, gm_id)
                get_player_stats.get_passing_info(bs_obj, gm_id)
                get_player_stats.get_rushing_info(bs_obj, gm_id)
                get_player_stats.get_receiving_info(bs_obj, gm_id)
                get_drive_info(bs_obj, gm_id, teams, year, week)
            if scrape_pbp:
                get_pbp(bs_obj, teams, year, week)
            print(f"Successfully scraped game {gm_id}")
            time.sleep(12)
        except Exception as e:
            print(f"Error scraping game {gm_id}: {e}")
            continue

