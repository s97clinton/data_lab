source("functions/normalize_carry_shares_functions.R")

### CINCINNATI RUSHING ###
rb1 <- TRUE
rusher1 <- run_ballcarrier_projections("Chase Brown", "Chase Brown", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Samaje Perine", "Samaje Perine", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Tahj Brooks", "Ray Davis", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['cin_joe_burrow']]==1, 'Joe Burrow', 'Jake Browning'), 
                                       ifelse(impact_players[['cin_joe_burrow']]==1, 'Joe Burrow', 'Jake Browning'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

