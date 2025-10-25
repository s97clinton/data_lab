source("functions/normalize_target_shares_functions.R")

### NEW YORK JETS RECEIVING ###
wr1 <- TRUE
wr1a <- FALSE
receiver1 <- run_pass_catcher_projections("Garrett Wilson", "Garrett Wilson", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver2 <- run_pass_catcher_projections("Mason Taylor", "Dalton Schultz", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver3 <- run_pass_catcher_projections("Josh Reynolds", "Josh Reynolds", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver4 <- run_pass_catcher_projections("Breece Hall", "Breece Hall", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver5 <- run_pass_catcher_projections("Jeremy Ruckert", "Jeremy Ruckert", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver6 <- run_pass_catcher_projections("Allen Lazard", "Allen Lazard", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver7 <- run_pass_catcher_projections("Braelon Allen", "Braelon Allen", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver8 <- run_pass_catcher_projections("Isaiah Davis", "Isaiah Davis", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver9 <- run_pass_catcher_projections("Stone Smartt", "Stone Smartt", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver10 <- run_pass_catcher_projections("Arian Smith", "Bo Melton", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)

team_receiving <- rbind(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
team_receiving <- normalize_team_target_share(team_receiving)
projected_target_distributions <- rbind(team_receiving, projected_target_distributions)

rm(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
