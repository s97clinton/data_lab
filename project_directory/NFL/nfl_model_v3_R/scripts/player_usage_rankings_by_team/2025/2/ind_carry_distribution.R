source("functions/normalize_carry_shares_functions.R")

### INDIANAPOLIS RUSHING ###
rb1 <- TRUE
rusher1 <- run_ballcarrier_projections("Jonathan Taylor", "Jonathan Taylor", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Khalil Herbert", "Khalil Herbert", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Tyler Goodson", "Tyler Goodson", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['ind_daniel_jones']]==1, 'Daniel Jones', 'Anthony Richardson'), 
                                       ifelse(impact_players[['ind_daniel_jones']]==1, 'Daniel Jones', 'Anthony Richardson'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

