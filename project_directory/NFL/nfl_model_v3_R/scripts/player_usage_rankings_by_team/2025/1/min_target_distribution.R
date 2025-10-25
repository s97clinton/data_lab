source("functions/normalize_target_shares_functions.R")

### MINNESOTA RECEIVING ###
wr1 <- TRUE
wr1a <- TRUE
receiver1 <- run_pass_catcher_projections("Justin Jefferson", "Justin Jefferson", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver2 <- run_pass_catcher_projections(ifelse(game_wk<4,"T.J. Hockenson","Jordan Addison"), ifelse(game_wk<4,"T.J. Hockenson","Jordan Addison"), ifelse(game_wk<4,"TE","WR"), matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver3 <- run_pass_catcher_projections(ifelse(game_wk<4,"Jalen Nailor","T.J. Hockenson"), ifelse(game_wk<4,"Jalen Nailor","T.J. Hockenson"), ifelse(game_wk<4,"WR","TE"), matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver4 <- run_pass_catcher_projections("Aaron Jones", "Aaron Jones", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver5 <- run_pass_catcher_projections(ifelse(game_wk<4,"Tai Felton","Jalen Nailor"), ifelse(game_wk<4,"Rondale Moore","Jalen Nailor"), "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver6 <- run_pass_catcher_projections("Josh Oliver", "Josh Oliver", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver7 <- run_pass_catcher_projections("Jordan Mason", "Jordan Mason", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver8 <- run_pass_catcher_projections(ifelse(game_wk<4,"Lucky Jackson","Tai Felton"), ifelse(game_wk<4,"Greg Dortch","Rondale Moore"), "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver9 <- run_pass_catcher_projections("Ty Chandler", "Ty Chandler", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver10 <- run_pass_catcher_projections("Nick Vannett", "Nick Vannett", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)

team_receiving <- rbind(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
team_receiving <- normalize_team_target_share(team_receiving)
projected_target_distributions <- rbind(team_receiving, projected_target_distributions)

rm(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
