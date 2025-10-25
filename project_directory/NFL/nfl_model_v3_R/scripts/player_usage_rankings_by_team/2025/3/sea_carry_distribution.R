source("functions/normalize_carry_shares_functions.R")

### SEATTLE RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Kenneth Walker III", "Kenneth Walker III", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Zach Charbonnet", "Zach Charbonnet", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("George Holani", "Pierre Strong", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['sea_sam_darnold']]==1, 'Sam Darnold', 'Drew Lock'), 
                                       ifelse(impact_players[['sea_sam_darnold']]==1, 'Sam Darnold', 'Drew Lock'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

