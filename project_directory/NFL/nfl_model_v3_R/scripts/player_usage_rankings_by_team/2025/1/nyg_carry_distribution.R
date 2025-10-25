source("functions/normalize_carry_shares_functions.R")

### NY GIANTS RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Tyrone Tracy Jr.", "Tyrone Tracy Jr.", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Cam Skattebo", "Rico Dowdle", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Devin Singletary", "Devin Singletary", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['nyg_russell_wilson']]==1, 'Russell Wilson', 'Jameis Winston'), 
                                       ifelse(impact_players[['nyg_russell_wilson']]==1, 'Russell Wilson', 'Jameis Winston'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

