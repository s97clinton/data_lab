source("functions/normalize_target_shares_functions.R")

### BUFFALO RECEIVING ###
wr1 <- FALSE
wr1a <- FALSE
receiver1 <- run_pass_catcher_projections("Khalil Shakir", "Khalil Shakir", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver2 <- run_pass_catcher_projections("Dalton Kincaid", "Dalton Kincaid", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver3 <- run_pass_catcher_projections("Keon Coleman", "Keon Coleman", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver4 <- run_pass_catcher_projections("Josh Palmer", "Josh Palmer", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver5 <- run_pass_catcher_projections("Dawson Knox", "Dawson Knox", "TE", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver6 <- run_pass_catcher_projections("Ty Johnson", "Ty Johnson", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver7 <- run_pass_catcher_projections("James Cook", "James Cook", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver8 <- run_pass_catcher_projections("Ray Davis", "Ray Davis", "RB", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver9 <- run_pass_catcher_projections("Curtis Samuel", "Curtis Samuel", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)
receiver10 <- run_pass_catcher_projections("Elijah Moore", "Elijah Moore", "WR", matchup, target_share_predictor, target_conv_predictor, yards_per_rec_predictor, td_share_predictor)

team_receiving <- rbind(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
team_receiving <- normalize_team_target_share(team_receiving)
projected_target_distributions <- rbind(team_receiving, projected_target_distributions)

rm(receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8, receiver9, receiver10)
