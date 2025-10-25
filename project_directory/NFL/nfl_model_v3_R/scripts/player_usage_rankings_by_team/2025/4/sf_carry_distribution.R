source("functions/normalize_carry_shares_functions.R")

### SAN FRANCISCO RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Christian McCaffrey", "Christian McCaffrey", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Brian Robinson Jr.", "Jordan Mason", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Isaac Guerendo", "Isaac Guerendo", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['sf_brock_purdy']]==1, 'Brock Purdy', 'Mac Jones'), 
                                       ifelse(impact_players[['sf_brock_purdy']]==1, 'Brock Purdy', 'Mac Jones'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

