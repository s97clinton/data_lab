source("functions/normalize_carry_shares_functions.R")

### CHICAGO RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("D'Andre Swift", "D'Andre Swift", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Roschon Johnson", "Roschon Johnson", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Travis Homer", "Travis Homer", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['chi_caleb_williams']]==1, 'Caleb Williams', 'Tyson Bagent'), 
                                       ifelse(impact_players[['chi_caleb_williams']]==1, 'Caleb Williams', 'Tyson Bagent'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

