source("functions/normalize_carry_shares_functions.R")

### DENVER RUSHING ###
rb1 <- TRUE
rusher1 <- run_ballcarrier_projections("R.J. Harvey", "Bucky Irving", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("J.K. Dobbins", "J.K. Dobbins", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Audric Estime", "Audric Estime", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['den_bo_nix']]==1, 'Bo Nix', 'Jarrett Stidham'), 
                                       ifelse(impact_players[['den_bo_nix']]==1, 'Bo Nix', 'Jarrett Stidham'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

