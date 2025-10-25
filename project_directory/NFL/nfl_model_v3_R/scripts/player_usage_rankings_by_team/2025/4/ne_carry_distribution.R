source("functions/normalize_carry_shares_functions.R")

### NEW ENGLAND RUSHING ###
rb1 <- TRUE
rusher1 <- run_ballcarrier_projections("TreVeyon Henderson", "Bucky Irving", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Rhamondre Stevenson", "Rhamondre Stevenson", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Antonio Gibson", "Kenneth Gainwell", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['ne_drake_maye']]==1, 'Drake Maye', 'Joshua Dobbs'), 
                                       ifelse(impact_players[['ne_drake_maye']]==1, 'Drake Maye', 'Joshua Dobbs'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

