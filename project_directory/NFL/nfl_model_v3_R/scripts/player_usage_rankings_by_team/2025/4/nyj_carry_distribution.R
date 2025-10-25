source("functions/normalize_carry_shares_functions.R")

### NY JETS RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Breece Hall", "Breece Hall", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Braelon Allen", "Braelon Allen", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Isaiah Davis", "Hassan Haskins", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['nyj_justin_fields']]==1, 'Justin Fields', 'Tyrod Taylor'), 
                                       ifelse(impact_players[['nyj_justin_fields']]==1, 'Justin Fields', 'Tyrod Taylor'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

