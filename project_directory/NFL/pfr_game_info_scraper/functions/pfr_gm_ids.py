import cloudscraper
from bs4 import BeautifulSoup
import time

def get_pfr_gm_ids(season: int, week: int) -> list:
    """
    Function: 
    - Retrieves the "game IDs" for a set of NFL games given the "season" and "week" parameters.

    Parameters:
    <season> (int): The NFL season of targeted games to scrape, passed as integer
    <week> (int): The NFL week of targeted games to scrape, passed as integer

    Returns:
    <game_ids> (list): A list containing the PFR "game IDs" for the requested subset.
    """
    url = f'https://www.pro-football-reference.com/years/{season}/week_{week}.htm'
    scraper = cloudscraper.create_scraper()  
    try:
        response = scraper.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Failed to retrieve page: {response.status_code} - {response.reason}")
            return []
        bsObj = BeautifulSoup(response.text, 'html.parser')
        game_ids = []
        for link in bsObj.find_all('td', {'class': 'right gamelink'}):
            href = link.find('a')['href']
            game_id = href.split('/')[-1].replace('.htm', '')
            game_ids.append(game_id)
        time.sleep(1)
        return game_ids
    except Exception as e:
        print(f"Error: {e}")
        return []