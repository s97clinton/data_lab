source("functions/normalize_carry_shares_functions.R")

### PITTSBURGH RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Kaleb Johnson", "Tyler Allgeier", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Jaylen Warren", "Jaylen Warren", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Kenneth Gainwell", "Kenneth Gainwell", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['pit_aaron_rodgers']]==1, 'Aaron Rodgers', 'Mason Rudolph'), 
                                       ifelse(impact_players[['pit_aaron_rodgers']]==1, 'Aaron Rodgers', 'Mason Rudolph'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

