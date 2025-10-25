source("functions/normalize_carry_shares_functions.R")

### PHILADELPHIA RUSHING ###
rb1 <- TRUE
rusher1 <- run_ballcarrier_projections("Saquon Barkley", "Saquon Barkley", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Will Shipley", "Kenneth Gainwell", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("AJ Dillon", "Pierre Strong", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['phi_jalen_hurts']]==1, 'Jalen Hurts', 'Sam Howell'), 
                                       ifelse(impact_players[['phi_jalen_hurts']]==1, 'Jalen Hurts', 'Sam Howell'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

