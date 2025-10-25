source("functions/normalize_target_shares_functions.R")

### WASHINGTON RECEIVING ###
wr1 <- TRUE
wr1a <- FALSE
receiver1 <- run_pass_catcher_projections("Terry McLaurin", "Terry McLaurin", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver2 <- run_pass_catcher_projections("Zach Ertz", "Zach Ertz", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver3 <- run_pass_catcher_projections("Deebo Samuel", "Deebo Samuel", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver4 <- run_pass_catcher_projections("Austin Ekeler", "Austin Ekeler", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver5 <- run_pass_catcher_projections("Noah Brown", "Noah Brown", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver6 <- run_pass_catcher_projections("Jacorey Croskey-Merritt", "Jordan Mason", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver7 <- run_pass_catcher_projections("Jaylin Lane", "Jalen Reagor", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver8 <- run_pass_catcher_projections("John Bates", "John Bates", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver9 <- run_pass_catcher_projections("Luke McCaffrey", "Luke McCaffrey", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver10 <- run_pass_catcher_projections("Chris Rodriguez", "Chris Rodriguez", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)

team_receiving <- rbind(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
team_receiving <- normalize_team_target_share(team_receiving)
projected_target_distributions <- rbind(team_receiving, projected_target_distributions)

rm(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
