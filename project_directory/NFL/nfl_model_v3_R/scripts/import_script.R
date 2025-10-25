source("functions/create_training_frames_by_outcome.R")
source("functions/data_transformation_functions.R")
source("functions/utils.R")

# Base .csv import
nfl_schedule <- import_schedule(if (length(model_params$projection_weeks) < 60) model_params$current_season else 'composite')
dvoa_merge <- import_historic_dvoa(model_params$start_season, model_params$current_season)
nfl_coaches_table <- import_nfl_coaches(model_params$start_season, model_params$current_season)

# Base MySQL import
pfr_game_basic <- import_pfr_game_basic(model_params$start_season, model_params$current_season)
pfr_gm_ids <- pfr_game_basic$game_id
pfr_team_stats <- import_pfr_team_stats(pfr_gm_ids)
pfr_pass_df <- import_pfr_pass_stats(pfr_gm_ids)
pfr_rush_df <- import_pfr_rush_stats(pfr_gm_ids)
pfr_rec_df <- import_pfr_rec_stats(pfr_gm_ids)
pfr_drive_df <- import_pfr_drive_data(model_params$start_season, model_params$current_season)

# Combine Data Sources to build live dataframes
pfr_team_stats <- build_team_stats_df(pfr_game_basic, pfr_team_stats, nfl_coaches_table)
pfr_drive_df <- build_pfr_drive_df(pfr_drive_df, dvoa_merge, nfl_coaches_table)
pfr_rush_df <- build_pfr_rush_df(pfr_rush_df, pfr_team_stats, dvoa_merge)
pfr_rush_df <- add_decay_dates(pfr_rush_df)
pfr_rec_df <- build_pfr_rec_df(pfr_rec_df, pfr_team_stats, dvoa_merge, nfl_coaches_table)
pfr_rec_df <- add_decay_dates(pfr_rec_df)

# Create Reference data
run_pass_ref_drive_df <- build_run_pass_ref_drive_df(pfr_drive_df)
drive_outcome_train_df <- pfr_drive_df
qtr_multipliers <- create_qtr_multipliers(pfr_drive_df)
td_ratio_df <- pfr_team_stats

#Create Training Frames
train_df_factors <- create_factor_outcomes(drive_outcome_train_df)
train_df_numeric <- create_numeric_outcomes(drive_outcome_train_df)
source("scripts/filter_run_pass_reference_data.R")
source("scripts/calculate_run_pass_ratios.R")

rm(user, password, connect_my_sql_db)
rm(pfr_gm_ids, dvoa_merge, nfl_coaches_table, create_qtr_multipliers)
rm(import_schedule, import_historic_dvoa, import_nfl_coaches,
   import_pfr_game_basic, import_pfr_team_stats, import_pfr_drive_data,
   import_pfr_pass_stats, import_pfr_rush_stats, import_pfr_rec_stats,
   create_factor_outcomes, create_numeric_outcomes)
