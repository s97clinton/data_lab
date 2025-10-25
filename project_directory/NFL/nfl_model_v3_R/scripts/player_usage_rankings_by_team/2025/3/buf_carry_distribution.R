source("functions/normalize_carry_shares_functions.R")

### BUFFALO RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("James Cook", "James Cook", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Ray Davis", "Ray Davis", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Ty Johnson", "Ty Johnson", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['buf_josh_allen']]==1, 'Josh Allen', 'Mitchell Trubisky'), 
                                       ifelse(impact_players[['buf_josh_allen']]==1, 'Josh Allen', 'Mitchell Trubisky'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

