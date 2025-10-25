library("foreign")
library("nnet")

run_multinomial_log_reg_model <- function (proj_df, train_df_factors, away_proj_df, home_proj_df) {
  multinomial_model <- multinom(drive_result_grouped ~ off_rating + def_rating + venue, data = train_df_factors, MaxNWts = 3000)
  predictions_away <- predict(multinomial_model, away_proj_df, type = "probs")
  predictions_home <- predict(multinomial_model, home_proj_df, type = "probs")
  
  away_df <- cbind(away_proj_df, predictions_away)
  home_df <- cbind(home_proj_df, predictions_home)
  
  away_df$away_proj_points <- round(((away_df$proj_drives*away_df$touchdown*7)+(away_df$proj_drives*away_df$fg*3)+(home_df$proj_drives*home_df$safety*2)), 2)
  home_df$home_proj_points <- round(((home_df$proj_drives*home_df$touchdown*7)+(home_df$proj_drives*home_df$fg*3)+(away_df$proj_drives*away_df$safety*2)), 2)
  
  away_df <- subset(away_df, select = c('key', 'away_proj_points'))
  home_df <- subset(home_df, select = c('key', 'home_proj_points'))
  
  proj_df <- merge(proj_df, away_df, on = 'key')
  proj_df <- merge(proj_df, home_df, on = 'key')
  
  proj_df$home_line <- round(proj_df$away_proj_points - proj_df$home_proj_points, 2)
  proj_df$total <- round(proj_df$away_proj_points + proj_df$home_proj_points, 2)
  
  return (proj_df)
}


