source("functions/normalize_carry_shares_functions.R")

### BALTIMORE RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Derrick Henry", "Derrick Henry", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Justice Hill", "Justice Hill", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Keaton Mitchell", "Keaton Mitchell", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['bal_lamar_jackson']]==1, 'Lamar Jackson', 'Cooper Rush'), 
                                       ifelse(impact_players[['bal_lamar_jackson']]==1, 'Lamar Jackson', 'Cooper Rush'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

