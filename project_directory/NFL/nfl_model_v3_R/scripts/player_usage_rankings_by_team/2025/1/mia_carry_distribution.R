source("functions/normalize_carry_shares_functions.R")

### MIAMI RUSHING ###
rb1 <- TRUE
rusher1 <- run_ballcarrier_projections("De'Von Achane", "De'Von Achane", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Jaylen Wright", "Jaylen Wright", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Alexander Mattison", "Alexander Mattison", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['mia_tua_tagovailoa']]==1, 'Tua Tagovailoa', 'Zach Wilson'), 
                                       ifelse(impact_players[['mia_tua_tagovailoa']]==1, 'Tua Tagovailoa', 'Zach Wilson'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

