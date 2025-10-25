source("functions/normalize_carry_shares_functions.R")

### LA CHARGERS RUSHING ###
rb1 <- TRUE
rusher1 <- run_ballcarrier_projections("Omarion Hampton", "James Conner", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Najee Harris", "Najee Harris", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Kimani Vidal", "Kimani Vidal", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['lac_justin_herbert']]==1, 'Justin Herbert', 'Taylor Heinicke'), 
                                       ifelse(impact_players[['lac_justin_herbert']]==1, 'Justin Herbert', 'Taylor Heinicke'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

