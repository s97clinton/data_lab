source("functions/normalize_carry_shares_functions.R")

### LAS VEGAS RAIDERS RUSHING ###
rb1 <- TRUE
rusher1 <- run_ballcarrier_projections("Ashton Jeanty", "Jonathan Taylor", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("Raheem Mostert", "Raheem Mostert", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Zamir White", "Zamir White", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['lvr_geno_smith']]==1, 'Geno Smith', "Kenny Pickett"), 
                                       ifelse(impact_players[['lvr_geno_smith']]==1, 'Geno Smith', "Kenny Pickett"), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

