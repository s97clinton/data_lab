source("functions/set_third_down_rates.R")
source("functions/set_average_drive_data.R")
source("functions/import_functions_current_week_ratings.R")
source("functions/create_test_frames_by_venue.R")

source("scripts/create_qb_keys.R")
proj_df <- nfl_schedule[(nfl_schedule$week==game_wk),]
proj_df$key <- paste(proj_df$away, proj_df$home, game_wk, model_params$current_season, sep = "_")
source("scripts/set_qb_rates.R")
proj_df <- set_third_down_rates(proj_df, pfr_team_stats)
proj_df <- set_average_drives_per_gm(proj_df, drive_outcome_train_df)
proj_df <- set_average_plays_per_drive(proj_df, drive_outcome_train_df)
proj_df <- set_average_run_pass_ratio_per_drive(proj_df, run_pass_ref_drive_df)
proj_df <- set_average_td_fg_ratio(proj_df, drive_outcome_train_df)
proj_df <- set_average_rush_pass_td_ratio(proj_df, td_ratio_df)

current_ratings <- import_current_ratings(model_params$current_season, game_wk)
away_proj_df <- create_test_set_away(proj_df, current_ratings)
home_proj_df <- create_test_set_home(proj_df, current_ratings)

rm(set_third_down_rates, set_average_drives_per_gm, set_average_plays_per_drive,
   set_average_run_pass_ratio_per_drive, set_average_td_fg_ratio, set_average_rush_pass_td_ratio)

