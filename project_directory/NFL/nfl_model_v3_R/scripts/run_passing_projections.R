agg_rec_stats <- aggregate(
  x = rec_stats_df[, c("targets", "receptions", "rec_yds", "rec_td")],
  by = list(key = rec_stats_df$key, team = rec_stats_df$team),
  FUN = sum,
  na.rm = TRUE
)

pass_stats_df <- rush_stats_df[(rush_stats_df$pos=="QB"),]
pass_stats_df <- subset(pass_stats_df, select = c("key", "team", "pos", "player_name"))
pass_stats_df <- merge(pass_stats_df, agg_rec_stats, by = c("key", "team"), all.x = TRUE)
colnames(pass_stats_df) <- c("key", "team", "pos", "player_name","pass_attempts", "completions", "pass_yds", "pass_td")

away_int <- subset(game_stat_df, select = c("key", "away", "away_proj_int"))
colnames(away_int) <- c("key", "team", "interceptions")
home_int <- subset(game_stat_df, select = c("key", "home", "home_proj_int"))
colnames(home_int) <- c("key", "team", "interceptions")
merge_int <- rbind(away_int, home_int)

pass_stats_df <- merge(pass_stats_df, merge_int, by = c("key", "team"), all.x = TRUE)
write.csv(pass_stats_df, paste0('result_dump/projected_fantasy_stats/projected_pass_stats/pass_stats_week_', game_wk,'.csv'))
