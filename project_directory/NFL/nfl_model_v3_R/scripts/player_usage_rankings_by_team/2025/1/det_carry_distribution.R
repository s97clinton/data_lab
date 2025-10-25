source("functions/normalize_carry_shares_functions.R")

### DETROIT RUSHING ###
rb1 <- FALSE
rusher1 <- run_ballcarrier_projections("Jahmyr Gibbs", "Jahmyr Gibbs", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher2 <- run_ballcarrier_projections("David Montgomery", "David Montgomery", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher3 <- run_ballcarrier_projections("Craig Reynolds", "Craig Reynolds", "RB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)
rusher4 <- run_ballcarrier_projections(ifelse(impact_players[['det_jared_goff']]==1, 'Jared Goff', 'Kyle Allen'), 
                                       ifelse(impact_players[['det_jared_goff']]==1, 'Jared Goff', 'Kyle Allen'), 
                                       "QB", matchup, carry_share_predictor, yards_per_carry_predictor, td_share_predictor)

team_rushing <- rbind(rusher1, rusher2, rusher3, rusher4)
team_rushing <- normalize_team_carry_share(team_rushing)
projected_carry_distributions <- rbind(team_rushing, projected_carry_distributions)

rm(rusher1, rusher2, rusher3, rusher4)

