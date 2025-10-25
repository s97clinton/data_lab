source("functions/normalize_carry_shares_functions.R")

### MINNESOTA RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Aaron Jones", "Aaron Jones", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Jordan Mason", "Jordan Mason", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Ty Chandler", "Ty Chandler", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['min_jj_mccarthy']]==1, 'J.J. McCarthy', 'Carson Wentz'), 
                                       ifelse(impact_players[['min_jj_mccarthy']]==1, 'Sam Darnold', 'Carson Wentz'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

