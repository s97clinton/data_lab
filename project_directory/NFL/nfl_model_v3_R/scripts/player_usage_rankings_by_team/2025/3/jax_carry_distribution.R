source("functions/normalize_carry_shares_functions.R")

### JACKSONVILLE RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Tank Bigsby", "Tank Bigsby", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Travis Etienne", "Travis Etienne", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Bhayshul Tuten", "Bucky Irving", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['jax_trevor_lawrence']]==1, 'Trevor Lawrence', 'Nick Mullens'), 
                                       ifelse(impact_players[['jax_trevor_lawrence']]==1, 'Trevor Lawrence', 'Nick Mullens'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

