calculate_game_stats <- function(model_output_df) {
  game_stat_df <- model_output_df
  game_stat_df$away_proj_plays <- round((game_stat_df$proj_drives)*game_stat_df$proj_away_avg_drive_plays, 2)
  game_stat_df$home_proj_plays <- round((game_stat_df$proj_drives)*game_stat_df$proj_home_avg_drive_plays, 2)
  game_stat_df$away_proj_runs <- round(game_stat_df$away_proj_plays*game_stat_df$proj_away_run_percentage, 2)
  game_stat_df$home_proj_runs <- round(game_stat_df$home_proj_plays*game_stat_df$proj_home_run_percentage, 2)
  game_stat_df$away_proj_dropbacks <- round(game_stat_df$away_proj_plays*(1-game_stat_df$proj_away_run_percentage), 2)
  game_stat_df$home_proj_dropbacks <- round(game_stat_df$home_proj_plays*(1-game_stat_df$proj_home_run_percentage), 2)
  game_stat_df$away_proj_targeted_pass_att <- round((game_stat_df$away_proj_dropbacks * (1 - game_stat_df$away_qb_sack_rate - 0.035)), 2)
  game_stat_df$home_proj_targeted_pass_att <- round((game_stat_df$home_proj_dropbacks * (1 - game_stat_df$home_qb_sack_rate - 0.035)), 2)
  game_stat_df$away_proj_td <- round(game_stat_df$away_proj_points*game_stat_df$proj_away_td_fg_percentage/7, 2)
  game_stat_df$home_proj_td <- round(game_stat_df$home_proj_points*game_stat_df$proj_home_td_fg_percentage/7, 2)
  game_stat_df$away_proj_rush_td <- round(game_stat_df$away_proj_td*game_stat_df$proj_away_rush_touchdown_perc, 2)
  game_stat_df$home_proj_rush_td <- round(game_stat_df$home_proj_td*game_stat_df$proj_home_rush_touchdown_perc, 2)
  game_stat_df$away_proj_pass_td <- round(game_stat_df$away_proj_td*(1-game_stat_df$proj_away_rush_touchdown_perc), 2)
  game_stat_df$home_proj_pass_td <- round(game_stat_df$home_proj_td*(1-game_stat_df$proj_home_rush_touchdown_perc), 2)
  game_stat_df$away_proj_int <- round(game_stat_df$away_proj_targeted_pass_att*game_stat_df$away_qb_int_rate, 2)
  game_stat_df$home_proj_int <- round(game_stat_df$home_proj_targeted_pass_att*game_stat_df$home_qb_int_rate, 2)
  
  return (game_stat_df)
}

calculate_team_stats <- function(game_stat_df) {
  away_df <- subset(game_stat_df, select = c("key","away","proj_drives","proj_away_avg_drive_plays","proj_away_run_percentage","proj_away_td_fg_percentage",
                                             "proj_away_rush_touchdown_perc","away_proj_points","away_proj_plays","away_proj_dropbacks","away_proj_targeted_pass_att",
                                             "away_proj_td","away_proj_rush_td","away_proj_pass_td","away_proj_int"))
  colnames(away_df) <- c("key","team","drives","avg_drive_plays","run_percentage","td_fg_percentage",
                         "rush_td_perc","points","plays","dropbacks","targeted_pass_att",
                         "td","rush_td","pass_td","int")
  home_df <- subset(game_stat_df, select = c("key","home","proj_drives","proj_home_avg_drive_plays","proj_home_run_percentage","proj_home_td_fg_percentage",
                                             "proj_home_rush_touchdown_perc","home_proj_points","home_proj_plays","home_proj_dropbacks","home_proj_targeted_pass_att",
                                             "home_proj_td","home_proj_rush_td","home_proj_pass_td","home_proj_int"))
  colnames(home_df) <- c("key","team","drives","avg_drive_plays","run_percentage","td_fg_percentage",
                         "rush_td_perc","points","plays","dropbacks","targeted_pass_att",
                         "td","rush_td","pass_td","int")
  team_fantasy_stats_df <- rbind(away_df, home_df)
  team_fantasy_stats_df$avg_drive_plays <- round(team_fantasy_stats_df$avg_drive_plays, 2)
  return(team_fantasy_stats_df)
}

aggregate_season_outcomes <- function(path, output_path) {
  files <- list.files(path = path, pattern = "*.csv", full.names = TRUE)
  all_data <- files %>%
    lapply(read.csv) %>%
    bind_rows()
  
  check_winner <- function(proj_pts_for, proj_pts_against) {
    ifelse(proj_pts_for > proj_pts_against, 1, 0)
  }
  
  away_agg <- all_data %>%
    mutate(win = check_winner(away_proj_points, home_proj_points)) %>%
    group_by(away) %>%
    summarize(
      total_proj_pts_for = sum(away_proj_points, na.rm = TRUE),
      total_proj_pts_against = sum(home_proj_points, na.rm = TRUE),
      total_wins = sum(win, na.rm = TRUE)
    ) %>%
    dplyr::rename(team = away)
  
  home_agg <- all_data %>%
    mutate(win = check_winner(home_proj_points, away_proj_points)) %>%
    group_by(home) %>%
    summarize(
      total_proj_pts_for = sum(home_proj_points, na.rm = TRUE),
      total_proj_pts_against = sum(away_proj_points, na.rm = TRUE),
      total_wins = sum(win, na.rm = TRUE)
    ) %>%
    dplyr::rename(team = home)
  
  season_df <- full_join(away_agg, home_agg, by = "team") %>%
    mutate(
      total_proj_pts_for = total_proj_pts_for.x + total_proj_pts_for.y,
      total_proj_pts_against = total_proj_pts_against.x + total_proj_pts_against.y,
      total_wins = total_wins.x + total_wins.y
    ) %>%
    select(team, total_proj_pts_for, total_proj_pts_against, total_wins)
  
  season_df$py_exp_win <- (season_df$total_proj_pts_for)**2.37/((season_df$total_proj_pts_for)**2.37+(season_df$total_proj_pts_against)**2.37)
  season_df$py_exp_win <- round(season_df$py_exp_win * 17,2)
  
  colnames(season_df) <- c('team','points_for','points_against','games_favored','expected_wins')
  
  season_df$points_for <- round(season_df$points_for,2)
  season_df$points_against <- round(season_df$points_against,2)
  
  write.csv(season_df, paste0(output_path))
}

aggregate_team_season_stats <- function(path, output_path) {
  files <- list.files(path = path, pattern = "*.csv", full.names = TRUE)
  team_data <- files %>%
    lapply(read.csv) %>%
    bind_rows()
  
  team_data <- team_data %>%
    group_by(team) %>%
    summarise(
      drives = sum(drives),
      avg_drive_plays = mean(avg_drive_plays),
      run_percentage = mean(run_percentage),
      plays = sum(plays),
      dropbacks = sum(dropbacks),
      targeted_pass_att = sum(targeted_pass_att),
      points = sum(points),
      td_fg_percentage = mean(td_fg_percentage),
      rush_td_perc = mean(rush_td_perc),
      td = sum(td),
      rush_td = sum(rush_td),
      pass_td = sum(pass_td),
      int = sum(int)
    )
  
  write.csv(team_data, paste0(output_path))
}