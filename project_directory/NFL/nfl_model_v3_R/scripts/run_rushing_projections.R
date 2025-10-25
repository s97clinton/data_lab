source("functions/rushing_model_functions.R")

train_rush_df <- build_initial_rush_train_frame(pfr_rush_df)
train_rush_df <- remove_player_history(train_rush_df)
train_rush_df <- create_usage_metrics(train_rush_df)
test_rush_home <- build_test_set_home(proj_df)
test_rush_away <- build_test_set_away(proj_df)

carry_share_predictor <- lm(carry_perc ~ player_name + off_rating + def_rating, train_rush_df, weights = weight)
yards_per_carry_predictor <- lm(yards_per_carry ~ player_name + off_rating + def_rating, train_rush_df, weights = weight)
td_share_predictor <- lm(rush_td_share ~ player_name + off_rating + def_rating, train_rush_df, weights = weight)

projected_carry_distributions <- data.frame(key = character(),team = character(),opp = character(),position = character(),name = character(),carry_share = numeric(),yards_per_carry = numeric(),rush_td_share = numeric(),stringsAsFactors = FALSE)

for (loop_team in model_params$nfl_teams) {
  matchup <- if (loop_team %in% test_rush_away$team) {
    test_rush_away %>%
      filter(team == loop_team)
  } else if (loop_team %in% test_rush_home$team) {
    test_rush_home %>%
      filter(team == loop_team)
  } else {
    NULL
  }
  
  if (!is.null(matchup)) {
    # print(matchup)
    # source(paste0("scripts/player_usage_rankings_by_team/",model_params$current_season,"/1/",tolower(loop_team),"_carry_distribution.R")) #static path to run in off-season
    source(paste0("scripts/player_usage_rankings_by_team/",model_params$current_season,"/",game_wk,"/",tolower(loop_team),"_carry_distribution.R"))
  }
}

away_merge <- subset(game_stat_df, select = c("key", "away", "away_proj_runs", "away_proj_rush_td"))
colnames(away_merge) <- c("key", "team", "tm_proj_runs", "tm_proj_rush_td")
home_merge <- subset(game_stat_df, select = c("key", "home", "home_proj_runs", "home_proj_rush_td"))
colnames(home_merge) <- c("key", "team", "tm_proj_runs", "tm_proj_rush_td")
merge_df <- rbind(away_merge, home_merge)

projected_carry_distributions <- merge(projected_carry_distributions, merge_df, by = c("key","team"), all.x = TRUE)

projected_carry_distributions$carries <- round(projected_carry_distributions$carry_share * projected_carry_distributions$tm_proj_runs, 2)
projected_carry_distributions$rush_yds <- round(projected_carry_distributions$carries * projected_carry_distributions$yards_per_carry, 2)
projected_carry_distributions$rush_td <- round(projected_carry_distributions$rush_td_share * projected_carry_distributions$tm_proj_rush_td, 2)

write.csv(projected_carry_distributions, paste0('result_dump/projected_fantasy_stats/projected_rush_stats/projected_carry_distributions_week_', game_wk,'.csv'))
rush_stats_df <- subset(projected_carry_distributions, select = c('key', 'team', 'pos', 'player_name', 'carry_share', 'carries', 'rush_yds', 'rush_td_share', 'rush_td'))


rm(build_initial_rush_train_frame, remove_player_history, create_usage_metrics,
   build_test_set_home, build_test_set_away, test_rush_home, test_rush_away)
