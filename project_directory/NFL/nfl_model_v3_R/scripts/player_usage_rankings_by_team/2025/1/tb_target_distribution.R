source("functions/normalize_target_shares_functions.R")

### TAMPA BAY RECEIVING ###
wr1 <- TRUE
wr1a <- TRUE
receiver1 <- run_pass_catcher_projections("Mike Evans", "Mike Evans", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver2 <- run_pass_catcher_projections("Bucky Irving", "Bucky Irving", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver3 <- run_pass_catcher_projections(ifelse(game_wk<3, "Emeka Egbuka", "Chris Godwin"), ifelse(game_wk<3, "Chris Godwin", "Chris Godwin"), "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver4 <- run_pass_catcher_projections(ifelse(game_wk<3, "Trey Palmer", "Emeka Egbuka"), ifelse(game_wk<3, "Trey Palmer", "Brandon Aiyuk"), "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver5 <- run_pass_catcher_projections("Cade Otton", "Cade Otton", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver6 <- run_pass_catcher_projections("Tez Johnson", "Kalif Raymond", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver7 <- run_pass_catcher_projections("Rachaad White", "Rachaad White", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver8 <- run_pass_catcher_projections("Sean Tucker", "Sean Tucker", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver9 <- run_pass_catcher_projections("Payne Durham", "Payne Durham", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver10 <- run_pass_catcher_projections("Sterling Shepard", "Sterling Shepard", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)

team_receiving <- rbind(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
team_receiving <- normalize_team_target_share(team_receiving)
projected_target_distributions <- rbind(team_receiving, projected_target_distributions)

rm(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
