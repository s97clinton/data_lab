source("functions/normalize_carry_shares_functions.R")

### WASHINGTON RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Austin Ekeler", "Austin Ekeler", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Jacorey Croskey-Merritt", "Jordan Mason", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Chris Rodriguez", "Chris Rodriguez", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['wsh_jayden_daniels']]==1, 'Jayden Daniels', 'Marcus Mariota'), 
                                       ifelse(impact_players[['wsh_jayden_daniels']]==1, 'Jayden Daniels', 'Marcus Mariota'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

