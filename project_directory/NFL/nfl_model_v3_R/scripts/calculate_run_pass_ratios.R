run_pass_ref_drive_df$count <- 1
run_pass_ref_drive_df$drives_per_gm <- 0.0
run_pass_ref_drive_df$pass_rate <- 0.0
run_pass_ref_drive_df$passes_per_drive <- 0.0
run_pass_ref_drive_df$runs_per_drive <- 0.0

for (team in model_params$nfl_teams){
  run_pass_home_df <- run_pass_ref_drive_df[(run_pass_ref_drive_df$venue=='home' & run_pass_ref_drive_df$off==team),]
  home_drives_per_gm <- aggregate(run_pass_home_df$count, by=list(run_pass_home_df$season,run_pass_home_df$week), FUN=sum)
  home_drives_per_gm <- mean(home_drives_per_gm$x)
  pass_rate_home <- sum(run_pass_home_df$drive_passes)/(sum(run_pass_home_df$drive_runs) + sum(run_pass_home_df$drive_passes))
  passes_per_drive_home <- mean(run_pass_home_df$drive_passes)
  runs_per_drive_home <- mean(run_pass_home_df$drive_runs)
  
  run_pass_ref_drive_df$drives_per_gm <- ifelse(run_pass_ref_drive_df$venue=='home' & run_pass_ref_drive_df$off==team,home_drives_per_gm,run_pass_ref_drive_df$drives_per_gm)
  run_pass_ref_drive_df$pass_rate <- ifelse(run_pass_ref_drive_df$venue=='home' & run_pass_ref_drive_df$off==team,pass_rate_home,run_pass_ref_drive_df$pass_rate)
  run_pass_ref_drive_df$passes_per_drive <- ifelse(run_pass_ref_drive_df$venue=='home' & run_pass_ref_drive_df$off==team,passes_per_drive_home,run_pass_ref_drive_df$passes_per_drive)
  run_pass_ref_drive_df$runs_per_drive <- ifelse(run_pass_ref_drive_df$venue=='home' & run_pass_ref_drive_df$off==team,runs_per_drive_home,run_pass_ref_drive_df$runs_per_drive)
  
  run_pass_away_df <- run_pass_ref_drive_df[(run_pass_ref_drive_df$venue=='away' & run_pass_ref_drive_df$off==team),]
  away_drives_per_gm <- aggregate(run_pass_away_df$count, by=list(run_pass_away_df$season,run_pass_away_df$week), FUN=sum)
  away_drives_per_gm <- mean(away_drives_per_gm$x)
  pass_rate_away <- sum(run_pass_away_df$drive_passes)/(sum(run_pass_away_df$drive_runs) + sum(run_pass_away_df$drive_passes))
  passes_per_drive_away <- mean(run_pass_away_df$drive_passes)
  runs_per_drive_away <- mean(run_pass_away_df$drive_runs)
  
  run_pass_ref_drive_df$drives_per_gm <- ifelse(run_pass_ref_drive_df$venue=='away' & run_pass_ref_drive_df$off==team,away_drives_per_gm,run_pass_ref_drive_df$drives_per_gm)
  run_pass_ref_drive_df$pass_rate <- ifelse(run_pass_ref_drive_df$venue=='away' & run_pass_ref_drive_df$off==team,pass_rate_away,run_pass_ref_drive_df$pass_rate)
  run_pass_ref_drive_df$passes_per_drive <- ifelse(run_pass_ref_drive_df$venue=='away' & run_pass_ref_drive_df$off==team,passes_per_drive_away,run_pass_ref_drive_df$passes_per_drive)
  run_pass_ref_drive_df$runs_per_drive <- ifelse(run_pass_ref_drive_df$venue=='away' & run_pass_ref_drive_df$off==team,runs_per_drive_away,run_pass_ref_drive_df$runs_per_drive)
}


#Create Total Plays Per Drive
run_pass_ref_drive_df$total_plays_per_drive <- run_pass_ref_drive_df$passes_per_drive + run_pass_ref_drive_df$runs_per_drive

team_run_pass_ratio_ref_table <- run_pass_ref_drive_df %>%
  group_by(off) %>%
  summarise(
    drives_per_gm = round(mean(drives_per_gm, na.rm = TRUE),2),
    pass_rate = round(mean(pass_rate, na.rm = TRUE),4),
    passes_per_drive = round(mean(passes_per_drive, na.rm = TRUE),2),
    runs_per_drive = round(mean(runs_per_drive, na.rm = TRUE),2),
    total_plays_per_drive = round(mean(total_plays_per_drive, na.rm = TRUE),2)
  )

#Cleanup 
rm(run_pass_away_df,run_pass_home_df,pass_rate_away,pass_rate_home,passes_per_drive_away,passes_per_drive_home,runs_per_drive_away,runs_per_drive_home,team,home_drives_per_gm,away_drives_per_gm)
