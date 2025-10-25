source("functions/normalize_carry_shares_functions.R")

### CAROLINA RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Chuba Hubbard", "Chuba Hubbard", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Rico Dowdle", "Rico Dowdle", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Trevor Etienne", "Justice Hill", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['car_bryce_young']]==1, 'Bryce Young', 'Andy Dalton'), 
                                       ifelse(impact_players[['car_bryce_young']]==1, 'Bryce Young', 'Andy Dalton'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

