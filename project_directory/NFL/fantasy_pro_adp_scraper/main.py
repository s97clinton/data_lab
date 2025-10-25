from fantasy_pros_scraper import scrape_fantasypros_rankings

if __name__ == "__main__":
    no_ppr_df = scrape_fantasypros_rankings(scoring_type='no_ppr')
    if no_ppr_df is not None:
        print(no_ppr_df.head())
        no_ppr_df.to_csv('current_consensus_rankings/no_ppr_consensus_rankings.csv', index=False)

    half_ppr_df = scrape_fantasypros_rankings(scoring_type='half_ppr')
    if half_ppr_df is not None:
        print(half_ppr_df.head())
        half_ppr_df.to_csv('current_consensus_rankings/half_ppr_consensus_rankings.csv', index=False)
        
    full_ppr_df = scrape_fantasypros_rankings(scoring_type='full_ppr')
    if full_ppr_df is not None:
        print(full_ppr_df.head())
        full_ppr_df.to_csv('current_consensus_rankings/full_ppr_consensus_rankings.csv', index=False)


