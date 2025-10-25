source("functions/normalize_target_shares_functions.R")

### BALTIMORE RECEIVING ###
wr1 <- TRUE
wr1a <- FALSE
receiver1 <- run_pass_catcher_projections("Zay Flowers", "Zay Flowers", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver2 <- run_pass_catcher_projections("Rashod Bateman", "Rashod Bateman", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver3 <- run_pass_catcher_projections("Mark Andrews", "Mark Andrews", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver4 <- run_pass_catcher_projections("Isaiah Likely", "Isaiah Likely", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver5 <- run_pass_catcher_projections("Justice Hill", "Justice Hill", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver6 <- run_pass_catcher_projections("Charlie Kolar", "Charlie Kolar", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver7 <- run_pass_catcher_projections("DeAndre Hopkins", "DeAndre Hopkins", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver8 <- run_pass_catcher_projections("Derrick Henry", "Derrick Henry", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver9 <- run_pass_catcher_projections("Tylan Wallace", "Tylan Wallace", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver10 <- run_pass_catcher_projections("Keaton Mitchell", "Keaton Mitchell", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)

team_receiving <- rbind(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
team_receiving <- normalize_team_target_share(team_receiving)
projected_target_distributions <- rbind(team_receiving, projected_target_distributions)

rm(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
