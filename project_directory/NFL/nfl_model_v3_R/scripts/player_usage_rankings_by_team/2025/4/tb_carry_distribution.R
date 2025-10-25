source("functions/normalize_carry_shares_functions.R")

### TAMPA BAY RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Bucky Irving", "Bucky Irving", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Rachaad White", "Rachaad White", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Sean Tucker", "Sean Tucker", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['tb_baker_mayfield']]==1, 'Baker Mayfield', 'Teddy Bridgewater'), 
                                       ifelse(impact_players[['tb_baker_mayfield']]==1, 'Baker Mayfield', 'Jacoby Brissett'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

