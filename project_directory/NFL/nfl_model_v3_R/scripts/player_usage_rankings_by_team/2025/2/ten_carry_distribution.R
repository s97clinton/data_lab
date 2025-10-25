source("functions/normalize_carry_shares_functions.R")

### TENNESSEE RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Tony Pollard", "Tony Pollard", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Tyjae Spears", "Tyjae Spears", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Julius Chestnut", "Julius Chestnut", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['ten_cam_ward']]==1, 'Cam Ward', 'Brandon Allen'), 
                                       ifelse(impact_players[['ten_cam_ward']]==1, 'Bryce Young', 'Brandon Allen'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

