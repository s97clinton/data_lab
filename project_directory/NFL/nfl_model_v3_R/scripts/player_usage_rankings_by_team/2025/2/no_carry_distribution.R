source("functions/normalize_carry_shares_functions.R")

### NEW ORLEANS RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Alvin Kamara", "Alvin Kamara", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Kendre Miller", "Kendre Miller", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Devin Neal", "Clyde Edwards-Helaire", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['no_spencer_rattler']]==1, 'Spencer Rattler', 'Tyler Shough'), 
                                       ifelse(impact_players[['no_spencer_rattler']]==1, 'Spencer Rattler', 'Derek Carr'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

