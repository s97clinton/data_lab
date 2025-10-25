
build_team_stats_df <- function(pfr_game_basic, pfr_team_stats, nfl_coaches_table) {
  pfr_team_stats <- merge(pfr_game_basic, pfr_team_stats, by = c("game_id","key","team"))
  pfr_team_stats <- merge(pfr_team_stats, subset(nfl_coaches_table, select = c("season", "week", "team", "designer_offense", "playcaller_offense", "primary_qb", "backup_qb")), by.x = c("team","season","week"), by.y = c("team","season","week"), all.x = TRUE)
  return (pfr_team_stats)
}

build_pfr_drive_df <- function(pfr_drive_df, dvoa_merge, nfl_coaches_table) {
  pfr_drive_df <- merge(pfr_drive_df, subset(dvoa_merge, select = c("team", "off_rating", "season")), by.x = c("off", "season"), by.y = c("team", "season"), all.x = TRUE)
  pfr_drive_df <- merge(pfr_drive_df, subset(dvoa_merge, select = c("team", "def_rating", "season")), by.x = c("def", "season"), by.y = c("team", "season"), all.x = TRUE)
  pfr_drive_df <- merge(pfr_drive_df, subset(nfl_coaches_table, select = c("season", "week", "team", "designer_offense", "playcaller_offense", "primary_qb", "backup_qb")), by.x = c("off","season","week"), by.y = c("team","season","week"), all.x = TRUE)
  return (pfr_drive_df)
}

build_run_pass_ref_drive_df <- function(pfr_drive_df) {
  run_pass_ref_drive_df <- pfr_drive_df
  run_pass_ref_drive_df <- run_pass_ref_drive_df[complete.cases(run_pass_ref_drive_df[, c("drive_passes", "drive_runs", "drive_penalties")]), ]
  run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$drive_passes > run_pass_ref_drive_df$drive_plays | run_pass_ref_drive_df$drive_runs > run_pass_ref_drive_df$drive_plays),]
  return (run_pass_ref_drive_df)
}

build_pfr_rush_df <- function(pfr_rush_df, pfr_team_stats, dvoa_merge) {
  pfr_rush_df <- merge(pfr_rush_df, subset(pfr_team_stats, select = c("game_id", "team", "rush_attempts", "rush_yards", "rush_touchdowns")), by = c("game_id", "team"), all.x = TRUE)
  pfr_rush_df <- rename(pfr_rush_df, rush_attempts = rush_attempts.x, tm_rush_attempts = rush_attempts.y, tm_rush_yards = rush_yards, tm_rush_touchdowns = rush_touchdowns)
  pfr_rush_df <- merge(pfr_rush_df, subset(dvoa_merge, select = c("team", "off_rating", "season")), by = c("team", "season"), all.x = TRUE)
  pfr_rush_df <- merge(pfr_rush_df, subset(dvoa_merge, select = c("team", "def_rating", "season")), by.x = c("opp", "season"), by.y = c("team", "season"), all.x = TRUE)
  return(pfr_rush_df)
}

build_pfr_rec_df <- function(pfr_rec_df, pfr_team_stats, dvoa_merge, nfl_coaches_table) {
  pfr_rec_df <- merge(pfr_rec_df, subset(pfr_team_stats, select = c("game_id", "team", "pass_completions", "pass_attempts", "pass_yards", "pass_touchdowns")), by = c("game_id", "team"), all.x = TRUE)
  pfr_rec_df <- rename(pfr_rec_df, tm_pass_completions = pass_completions, tm_pass_attempts = pass_attempts,  tm_pass_yards = pass_yards, tm_pass_touchdowns = pass_touchdowns)
  pfr_rec_df <- merge(pfr_rec_df, subset(dvoa_merge, select = c("team", "off_rating", "season")), by = c("team", "season"), all.x = TRUE)
  pfr_rec_df <- merge(pfr_rec_df, subset(dvoa_merge, select = c("team", "def_rating", "season")), by.x = c("opp", "season"), by.y = c("team", "season"), all.x = TRUE)
  pfr_rec_df <- merge(pfr_rec_df, subset(nfl_coaches_table, select = c("season", "week", "team", "designer_offense", "playcaller_offense", "primary_qb", "backup_qb")), by.x = c("team","season","week"), by.y = c("team","season","week"), all.x = TRUE)
  return(pfr_rec_df)
}
