source("functions/normalize_carry_shares_functions.R")

### DALLAS RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Javonte Williams", "Javonte Williams", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Miles Sanders", "Miles Sanders", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Jaydon Blue", "Justice Hill", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['dal_dak_prescott']]==1, 'Dak Prescott', 'Joe Milton'), 
                                       ifelse(impact_players[['dal_dak_prescott']]==1, 'Dak Prescott', 'Tyrod Taylor'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

