source("functions/normalize_carry_shares_functions.R")

### ATLANTA RUSHING ###
rb1 <- TRUE
rusher1 <- run_ballcarrier_projections("Bijan Robinson", "Bijan Robinson", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Tyler Allgeier", "Tyler Allgeier", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Carlos Washington", "Pierre Strong", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['atl_michael_penix']]==1, 'Michael Penix', 'Kirk Cousins'), 
                                       ifelse(impact_players[['atl_michael_penix']]==1, 'Michael Penix', 'Kirk Cousins'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

