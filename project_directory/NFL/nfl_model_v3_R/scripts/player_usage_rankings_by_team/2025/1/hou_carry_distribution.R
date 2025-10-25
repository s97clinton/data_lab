source("functions/normalize_carry_shares_functions.R")

### HOUSTON RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Joe Mixon", "Joe Mixon", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Woody Marks", "James Cook", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Nick Chubb", "Nick Chubb", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['hou_cj_stroud']]==1, 'C.J. Stroud', 'Davis Mills'), 
                                       ifelse(impact_players[['hou_cj_stroud']]==1, 'C.J. Stroud', 'Davis Mills'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

