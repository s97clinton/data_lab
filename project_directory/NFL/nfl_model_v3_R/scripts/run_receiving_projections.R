source("functions/receiving_model_functions.R")

train_rec_df <- build_initial_rec_train_frame(pfr_rec_df)
train_rec_df <- remove_player_history(train_rec_df)
train_rec_df <- create_usage_metrics(train_rec_df)
test_rec_home <- build_test_set_home(proj_df)
test_rec_away <- build_test_set_away(proj_df)

target_share_predictor <- lm(tgt_share ~ player_name + off_rating + def_rating, train_rec_df, weights = weight)
target_conv_predictor <- lm(tgt_conv ~ player_name + off_rating + def_rating, train_rec_df, weights = weight)
yards_per_rec_predictor <- lm(yards_per_rec ~ player_name + off_rating + def_rating, train_rec_df, weights = weight)
td_share_predictor <- lm(rec_td_share ~ player_name + off_rating + def_rating, train_rec_df, weights = weight)

projected_target_distributions <- data.frame(key = character(),team = character(),opp = character(),position = character(),name = character(),tgt_share = numeric(),tgt_conv = numeric(),yards_per_rec = numeric(),rec_td_share = numeric(),stringsAsFactors = FALSE)

for (loop_team in model_params$nfl_teams) {
  matchup <- if (loop_team %in% test_rec_away$team) {
    test_rec_away %>%
      filter(team == loop_team)
  } else if (loop_team %in% test_rec_home$team) {
    test_rec_home %>%
      filter(team == loop_team)
  } else {
    NULL
  }
  
  if (!is.null(matchup)) {
    # print(matchup)
    # source(paste0("scripts/player_usage_rankings_by_team/",model_params$current_season,"/1/",tolower(loop_team),"_target_distribution.R")) #static path to run in off-season
    source(paste0("scripts/player_usage_rankings_by_team/",model_params$current_season,"/",game_wk,"/",tolower(loop_team),"_target_distribution.R"))
  }
}

away_merge <- subset(game_stat_df, select = c("key", "away", "away_proj_targeted_pass_att", "away_proj_pass_td"))
colnames(away_merge) <- c("key", "team", "tm_proj_targeted_pass_att", "tm_proj_pass_td")
home_merge <- subset(game_stat_df, select = c("key", "home", "home_proj_targeted_pass_att", "home_proj_pass_td"))
colnames(home_merge) <- c("key", "team", "tm_proj_targeted_pass_att", "tm_proj_pass_td")
merge_df <- rbind(away_merge, home_merge)

projected_target_distributions <- merge(projected_target_distributions, merge_df, by = c("key","team"), all.x = TRUE)
projected_target_distributions$targets <- round(projected_target_distributions$tgt_share * projected_target_distributions$tm_proj_targeted_pass_att, 2)
projected_target_distributions$receptions <- round(projected_target_distributions$tgt_share * projected_target_distributions$tgt_conv_rate * projected_target_distributions$tm_proj_targeted_pass_att, 2)
projected_target_distributions$rec_yds <- round(projected_target_distributions$receptions * projected_target_distributions$yards_per_rec, 2)
projected_target_distributions$rec_td <- round(projected_target_distributions$rec_td_share * projected_target_distributions$tm_proj_pass_td, 2)

write.csv(projected_target_distributions, paste0('result_dump/projected_fantasy_stats/projected_rec_stats/projected_target_distributions_week_', game_wk,'.csv'))
rec_stats_df <- subset(projected_target_distributions, select = c('key', 'team', 'pos', 'player_name', 'tgt_share', 'targets', 'receptions', 'rec_yds', 'rec_td_share', 'rec_td'))

rm(build_initial_rec_train_frame, remove_player_history, create_usage_metrics,
   build_test_set_home, build_test_set_away, test_rec_home, test_rec_away)
