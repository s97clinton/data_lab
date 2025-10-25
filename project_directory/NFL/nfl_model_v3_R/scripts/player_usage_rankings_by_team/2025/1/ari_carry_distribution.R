source("functions/normalize_carry_shares_functions.R")

### ARIZONA RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("James Conner", "James Conner", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Trey Benson", "Trey Benson", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Emari Demercado", "Emari Demercado", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['ari_kyler_murray']]==1, 'Kyler Murray', 'Jacoby Brissett'), 
                                       ifelse(impact_players[['ari_kyler_murray']]==1, 'Kyler Murray', 'Jacoby Brissett'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

