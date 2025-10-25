import pandas as pd
from datetime import datetime, timedelta

def create_composite_nfl_schedule():
    """
    Function:
    - Create a double round-robin NFL schedule for 32 teams over 62 weeks.
    - Each team plays every other team twice (once home, once away).
    - Ensure no team plays more than one game per week.
    - Takes the list of teams, number of teams, total weeks for each team to play all others twice,
      and generates a balanced schedule.
    - The output is used as a baseline to project how NFL teams would perform against a "balanced" schedule;
    this is compared against projections for the actual NFL schedule to assess the "strength" of schedule.

    Parameters:
    - None

    Returns:
    - DataFrame containing "composite" NFL schedule.
    """
    teams = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 
             'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC', 'LAC', 'LAR', 'LVR', 'MIA', 
             'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 
             'TEN', 'WSH']
    
    n = len(teams)  # 32 teams
    weeks = 2 * (n - 1)  # 62 weeks for double round-robin
    games_per_week = n // 2  # 16 games per week
    schedule = []

    # First round-robin (Weeks 1 to 31)
    for week in range(n - 1):
        weekly_games = []
        # Fix team 1 and pair with the last team
        # Home/away alternates based on week number for balance
        if week % 2 == 0:
            weekly_games.append((teams[0], teams[n-1]))  # T1 @ T32
        else:
            weekly_games.append((teams[n-1], teams[0]))  # T32 @ T1

        # Pair the remaining teams
        for i in range(1, games_per_week):
            team_a = teams[i]
            team_b = teams[n-1-i]
            # Alternate home/away for balance
            if (week + i) % 2 == 0:
                weekly_games.append((team_a, team_b))  # team_a @ team_b
            else:
                weekly_games.append((team_b, team_a))  # team_b @ team_a

        schedule.append(weekly_games)
        
        # Rotate teams[1:] (keep T1 fixed)
        teams = [teams[0]] + [teams[n-1]] + list(teams[1:n-1])

    # Second round-robin (Weeks 32 to 62): reverse home/away
    for week in range(n - 1):
        weekly_games = []
        for game in schedule[week]:
            # Reverse home/away from the first round-robin
            weekly_games.append((game[1], game[0]))  # Swap home and away
        schedule.append(weekly_games)

    start_date = datetime(2025, 9, 7)
    data = []
    for week in range(weeks):
        week_date = start_date + timedelta(days=7 * week)
        for away, home in schedule[week]:
            data.append({
                'week': week + 1,
                'date': week_date,
                'away': away,
                'home': home
            })
    
    df = pd.DataFrame(data)

    game_count = {team: {"home": 0, "away": 0, "opponents": set()} for team in teams}
    for week in range(weeks):
        week_teams = set()
        for _, row in df[df['week'] == week + 1].iterrows():
            away, home = row['away'], row['home']
            assert away not in week_teams and home not in week_teams, f"Team plays twice in week {week + 1}: {away}, {home}"
            week_teams.add(away)
            week_teams.add(home)
            game_count[away]["away"] += 1
            game_count[home]["home"] += 1
            game_count[away]["opponents"].add(home)
            game_count[home]["opponents"].add(away)
    
    for team in teams:
        assert game_count[team]["home"] == 31, f"{team} has {game_count[team]['home']} home games, expected 31"
        assert game_count[team]["away"] == 31, f"{team} has {game_count[team]['away']} away games, expected 31"
        assert len(game_count[team]["opponents"]) == 31, f"{team} played {len(game_count[team]['opponents'])} opponents, expected 31"

    return df

if __name__ == "__main__":
    schedule_df = create_composite_nfl_schedule()
    print(schedule_df.head(20))
    schedule_df.to_csv('nfl_schedule_2025.csv', index=False)