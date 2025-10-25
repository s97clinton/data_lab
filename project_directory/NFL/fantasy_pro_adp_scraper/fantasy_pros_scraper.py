from selenium import webdriver
from selenium.webdriver.safari.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def scrape_fantasypros_rankings(scoring_type:str='half_ppr'):
    """
    Function:
    -Scrapes the NFL Fantasy rankings table from FantasyPros using Selenium with Safari.
    
    Args:
    <scoring_type>: String denoting whether we want to pull no_ppr, half_ppr, or full_ppr. Defaults to 'half_ppr'
    
    Returns:
    <df>: DataFrame containing the cleaned rankings table.
    """
    if scoring_type not in (['no_ppr','half_ppr','full_ppr']):
        print("Unrecognized scoring type, please check your parameters.")
    elif scoring_type == 'no_ppr':
        url="https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php"
    elif scoring_type == 'full_ppr':
        url="https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php"
    else:
        url="https://www.fantasypros.com/nfl/rankings/half-point-ppr-cheatsheets.php"

    try:
        # Set up Selenium WebDriver for Safari
        service = Service()
        options = webdriver.SafariOptions()
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15')
        
        driver = webdriver.Safari(service=service, options=options)
        
        # Load the page
        driver.get(url)
        
        # Wait for the table to load
        time.sleep(3)  # Adjust if needed
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Close the browser
        driver.quit()
        
        # Find the table by its correct ID
        table = soup.find('table', {'id': 'ranking-table'})
        if not table:
            raise ValueError("Could not find the rankings table on the page.")
        
        # Extract headers
        headers = []
        thead = table.find('thead')
        if thead:
            header_row = thead.find('tr')
            headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
        
        # Extract table rows
        data = []
        tbody = table.find('tbody')
        if tbody:
            for row in tbody.find_all('tr'):
                cols = row.find_all('td')
                row_data = [col.get_text(strip=True) for col in cols]
                
                if len(row_data) < len(headers):
                    row_data.extend([None] * (len(headers) - len(row_data)))
                data.append(row_data)
        
        # Build Extracted Data into DataFrame
        df = pd.DataFrame(data, columns=headers if headers else [f"Column_{i+1}" for i in range(len(data[0]))])
        df = df[['RK','Player Name','POS','BYE WEEK']]# Add Tier column and clean up
        df['Tier'] = None
        current_tier = None
        
        for index, row in df.iterrows():
            if 'Tier' in row['RK']:
                current_tier = row['RK']  # Update current tier (e.g., 'Tier 1', 'Tier 2')
            elif row['Player Name'] != 'Customize Tiers' and current_tier:
                df.at[index, 'Tier'] = current_tier  # Assign tier to player rows
        
        # Drop rows where Player Name is 'Customize Tiers' and reset the index
        df = df[df['Player Name'] != 'Customize Tiers']
        df = df.reset_index(drop=True)

        # Extract team from Player Name using regex
        df['Team'] = df['Player Name'].str.extract(r'\((...|..)\)$')  # Matches 2 or 3 letters in parentheses at the end
        df['Player Name'] = df['Player Name'].str.replace(r'\s*\(...\)$', '', regex=True)  # Remove the three letter team in parentheses
        df['Player Name'] = df['Player Name'].str.replace(r'\s*\(..\)$', '', regex=True)  # Remove the two letter team in parentheses
        
        df = df.rename(columns={'RK':'ovr_rank','Player Name':'player','POS':'pos_rank','BYE WEEK':'bye','Tier':'tier','Team':'team'})
        df = df[['team','player','tier','ovr_rank','pos_rank','bye']]

        return df
    
    except Exception as e:
        print(f"Error processing the data: {e}")
        return None