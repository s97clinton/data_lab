source("functions/normalize_carry_shares_functions.R")

### KANSAS CITY RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Isiah Pacheco", "Isiah Pacheco", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Kareem Hunt", "Kareem Hunt", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Carson Steele", "Carson Steele", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['kc_pat_mahomes']]==1, 'Patrick Mahomes', 'Gardner Minshew II'), 
                                       ifelse(impact_players[['kc_pat_mahomes']]==1, 'Patrick Mahomes', 'Gardner Minshew II'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

