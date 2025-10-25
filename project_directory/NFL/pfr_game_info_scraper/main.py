from functions.pfr_gm_ids import get_pfr_gm_ids
from functions.pfr_scraper import scrape_pfr_game_pages

def nfl_pfr_collector(year_min: int, year_max: int, week_min: int, week_max: int, all_stats: bool, scrape_pbp: bool) -> None:
    """
    Function: Collects game information from Pro Football Reference (PFR) for the NFL.
    This function retrieves game IDs for a specified year and week, then scrapes the game pages
    to collect detailed statistics and play-by-play data.

    Parameters:
    <year_min> (int): Integer denoting starting year for data collection.
    <year_max> (int): The ending year for data collection.
    <week_min> (int): The starting week for data collection.
    <week_max> (int): The ending week for data collection.
    <all_stats> (Boolean): A Boolean marking whether or not the user wants to aquire the full
    set of statistics, or just the box score.
    <scrape_pbp> (Boolean): A Boolean marking whether or not the user wants to scrape the play-by-play data.

    Returns:
    None: This function does not return any value. It performs data scraping and saves the results
    to a MySQL database.
    """
    for year in range(year_min, year_max + 1):
        for week in range(week_min, week_max + 1):
            game_ids = get_pfr_gm_ids(year, week)
            scrape_pfr_game_pages(game_ids, year, week, all_stats = all_stats, scrape_pbp = scrape_pbp)

if __name__ == '__main__':
    nfl_pfr_collector(2025, 2025, 8, 8, all_stats = False, scrape_pbp = True)
    print("NFL PFR Game Info Scraper Complete")