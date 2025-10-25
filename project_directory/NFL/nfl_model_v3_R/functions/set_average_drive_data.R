library(dplyr)
library(tidyr)

set_average_drives_per_gm <- function(proj_df, run_pass_ref_drive_df) {
  
  team_drives_per_gm <- subset(run_pass_ref_drive_df, select = c('season','week','off'))
  team_drives_per_gm <- team_drives_per_gm %>%
    group_by(season, week, off) %>%
    summarise(count = n())
  team_drives_per_gm <- team_drives_per_gm %>%
    group_by(off) %>%
    summarise(average_count = round(mean(count),2))
  
  away_drives_per_gm <- team_drives_per_gm
  colnames(away_drives_per_gm) <- c('away','proj_away_drives')
  home_drives_per_gm <- team_drives_per_gm
  colnames(home_drives_per_gm) <- c('home','proj_home_drives')
  
  proj_df <- merge(proj_df, away_drives_per_gm, by = "away")
  proj_df <- merge(proj_df, home_drives_per_gm, by = "home")
  
  proj_df$proj_drives <- round(((proj_df$proj_away_drives + proj_df$proj_home_drives)/2), 2)
  
  return (proj_df)
}

set_average_plays_per_drive <- function(proj_df, run_pass_ref_drive_df) {
  
  filter_df <- subset(run_pass_ref_drive_df, select = c('off', 'drive_plays'))
  
  plays_per_drive_df <- filter_df %>%
    group_by(off) %>%
    summarise(avg_drive_plays = mean(as.numeric(drive_plays)))
  
  plays_per_drive_df$avg_drive_plays <- round(((0.5 * plays_per_drive_df$avg_drive_plays) + (0.5 * mean(plays_per_drive_df$avg_drive_plays))), 3)
  plays_per_drive_df <- subset(plays_per_drive_df, select = c('off', 'avg_drive_plays'))
  
  away_plays_per_drive_df <- plays_per_drive_df
  colnames(away_plays_per_drive_df) <- c('away', 'proj_away_avg_drive_plays')
  home_plays_per_drive_df <- plays_per_drive_df
  colnames(home_plays_per_drive_df) <- c('home', 'proj_home_avg_drive_plays')
  
  proj_df <- merge(proj_df, away_plays_per_drive_df, by='away')
  proj_df <- merge(proj_df, home_plays_per_drive_df, by='home')
  
  return (proj_df)
}

set_average_run_pass_ratio_per_drive <- function(proj_df, run_pass_ref_drive_df) {
  
  filter_df <- subset(run_pass_ref_drive_df, select = c('off', 'drive_passes', 'drive_runs'))
  
  run_pass_df <- filter_df %>%
    group_by(off) %>%
    summarise(avg_drive_pass_att = mean(drive_passes), avg_drive_rush_att = mean(drive_runs))
  run_pass_df$run_percentage <- round(run_pass_df$avg_drive_rush_att / (run_pass_df$avg_drive_pass_att + run_pass_df$avg_drive_rush_att), 2)
  
  run_pass_df <- subset(run_pass_df, select = c('off', 'run_percentage'))
  away_run_pass <- run_pass_df
  colnames(away_run_pass) <- c('away', 'proj_away_run_percentage')
  home_run_pass <- run_pass_df
  colnames(home_run_pass) <- c('home', 'proj_home_run_percentage')
  
  proj_df <- merge(proj_df, away_run_pass, by='away')
  proj_df <- merge(proj_df, home_run_pass, by='home')
  
  return (proj_df)
}

set_average_td_fg_ratio <- function(proj_df, run_pass_ref_drive_df) {
  reference_df <- subset(run_pass_ref_drive_df, select = c('off', 'drive_result'))
  reference_df <- reference_df[(reference_df$drive_result=='Touchdown' | reference_df$drive_result=='Field Goal'),]
  reference_df <- reference_df %>%
    group_by(off, drive_result) %>%
    summarise(count = n()) %>%
    pivot_wider(names_from = drive_result, values_from = count, values_fill = 0)
  
  reference_df$td_percentage <- round((reference_df$Touchdown*7)/((reference_df$Touchdown*7) + (reference_df$`Field Goal`*3)), 2)
  reference_df$td_percentage <- round(((0.8*reference_df$td_percentage) + (0.2*mean(reference_df$td_percentage))), 3)
  reference_df <- subset(reference_df, select=c('off','td_percentage'))
  
  away_scoring_df <- reference_df
  colnames(away_scoring_df) <- c('away', 'proj_away_td_fg_percentage')
  home_scoring_df <- reference_df
  colnames(home_scoring_df) <- c('home', 'proj_home_td_fg_percentage')
  
  proj_df <- merge(proj_df, away_scoring_df, by='away')
  proj_df <- merge(proj_df, home_scoring_df, by='home')
  
  return (proj_df)
}

set_average_rush_pass_td_ratio <- function(proj_df, pfr_team_stats) {
  away_td_df <- subset(pfr_team_stats, select = c('team','pass_touchdowns','rush_touchdowns'))
  
  away_td_df <- away_td_df %>%
    filter(!is.na(pass_touchdowns))
  away_td_df <- away_td_df %>%
    filter(!is.na(rush_touchdowns))
  
  away_td_df <- away_td_df %>%
    group_by(team) %>%
    summarise(total_pass_touchdowns = sum(as.numeric(pass_touchdowns)), total_rush_touchdowns = sum(as.numeric(rush_touchdowns)))
  
  away_td_df$rush_touchdown_perc <- round(as.numeric(away_td_df$total_rush_touchdowns)/(as.numeric(away_td_df$total_pass_touchdowns) + as.numeric(away_td_df$total_rush_touchdowns)),2)
  away_td_df$rush_touchdown_perc <- round(((0.75*away_td_df$rush_touchdown_perc) + (0.25*mean(away_td_df$rush_touchdown_perc))), 3)
  away_td_df$rush_touchdown_perc <- ifelse(away_td_df$rush_touchdown_perc<0.32, 0.32, away_td_df$rush_touchdown_perc)
  away_td_df <- subset(away_td_df, select = c('team','rush_touchdown_perc'))
  colnames(away_td_df) <- c('away','proj_away_rush_touchdown_perc')
  
  home_td_df <- subset(pfr_team_stats, select = c('team','pass_touchdowns','rush_touchdowns'))
  
  home_td_df <- home_td_df %>%
    filter(!is.na(pass_touchdowns))
  home_td_df <- home_td_df %>%
    filter(!is.na(rush_touchdowns))
  
  home_td_df <- home_td_df %>%
    group_by(team) %>%
    summarise(total_pass_touchdowns = sum(as.numeric(pass_touchdowns)), total_rush_touchdowns = sum(as.numeric(rush_touchdowns)))
  
  home_td_df$rush_touchdown_perc <- round(as.numeric(home_td_df$total_rush_touchdowns)/(as.numeric(home_td_df$total_pass_touchdowns) + as.numeric(home_td_df$total_rush_touchdowns)),2)
  home_td_df$rush_touchdown_perc <- round(((0.75*home_td_df$rush_touchdown_perc) + (0.25*mean(home_td_df$rush_touchdown_perc))), 3)
  home_td_df$rush_touchdown_perc <- ifelse(home_td_df$rush_touchdown_perc<0.32, 0.32, home_td_df$rush_touchdown_perc)
  home_td_df <- subset(home_td_df, select = c('team','rush_touchdown_perc'))
  colnames(home_td_df) <- c('home','proj_home_rush_touchdown_perc')
  
  proj_df <- merge(proj_df, away_td_df, by = "away")
  proj_df <- merge(proj_df, home_td_df, by = "home")
  
  return (proj_df)
}