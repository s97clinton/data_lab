setwd("~/Documents/_sjc_repo_/data_lab/project_directory/NFL/nfl_model_v3_R")

source("functions/import_functions.R")
source("functions/run_multinomial_log_reg_model.R")
source("functions/calculate_game_stats.R")
source("functions/build_fantasy_boards.R")

model_start_time <- Sys.time()
model_params <- set_model_parameters(2025, 10, 11) #run 1-62 for composite schedule
source("scripts/import_script.R")

for (game_wk in model_params$projection_weeks) {
  source("scripts/build_projection_df.R")
  multinomial_model_output <- run_multinomial_log_reg_model(proj_df, train_df_factors, away_proj_df, home_proj_df)
  game_stat_df <- calculate_game_stats(multinomial_model_output)
  condensed_multinomial_output <- subset(multinomial_model_output, select = c("date","week","away","home","away_qb","home_qb","away_proj_points","home_proj_points", "home_line", "total"))
  write.csv(condensed_multinomial_output, paste0("result_dump/projected_weekly_game_outcomes/game_outcomes_week_", game_wk,".csv"))
  
  if (model_params$fantasy_player_projection==1) {
    team_fantasy_stats_df <- calculate_team_stats(game_stat_df)
    write.csv(team_fantasy_stats_df, paste0("result_dump/projected_fantasy_stats/projected_team_fantasy/fantasy_team_stat_df_week_", game_wk,".csv"))
    write.csv(game_stat_df, paste0("result_dump/projected_fantasy_stats/projected_team_stats/fantasy_stat_df_week_", game_wk,".csv"))
    source("scripts/run_rushing_projections.R")
    source("scripts/run_receiving_projections.R")
    source("scripts/run_passing_projections.R")
    qb_board <- build_qb_board(pass_stats_df, rush_stats_df)
    skill_board <- build_skill_board(rush_stats_df, rec_stats_df)
    write.csv(qb_board, paste0("result_dump/projected_fantasy_stats/qb_board/qb_board_week_", game_wk,".csv"))
    write.csv(skill_board, paste0("result_dump/projected_fantasy_stats/skill_board/skill_board_week_", game_wk,".csv"))
  }
  cat("Week ", game_wk, " Complete\n")
  
}

source("scripts/results_aggregator.R")

model_end_time <- Sys.time()
cat("Time:", model_end_time - model_start_time, "\n")


