create_test_set_away <- function(proj_df, current_ratings) {
  away_proj_df <- subset(proj_df, select = c(away, home, key, proj_drives))
  colnames(away_proj_df) <- c('off', 'def', 'key', 'proj_drives')
  away_proj_df$venue <- as.factor('away')
  away_proj_df$off_rating <- 0.0
  away_proj_df$def_rating <- 0.0
  
  for (team in model_params$nfl_teams){
    team_data <- current_ratings[(current_ratings$team==team),]
    away_proj_df$off_rating <- ifelse(away_proj_df$off==team, team_data$off_rating, away_proj_df$off_rating)
    away_proj_df$def_rating <- ifelse(away_proj_df$def==team, team_data$def_rating, away_proj_df$def_rating)
  }
  
  return (away_proj_df)
}

create_test_set_home <- function(proj_df, current_ratings) {
  home_proj_df <- subset(proj_df, select = c(home, away, key, proj_drives))
  colnames(home_proj_df) <- c('off', 'def', 'key', 'proj_drives')
  home_proj_df$venue <- as.factor('home')
  home_proj_df$off_rating <- 0.0
  home_proj_df$def_rating <- 0.0
  
  for (team in model_params$nfl_teams){
    team_data <- current_ratings[(current_ratings$team==team),]
    home_proj_df$off_rating <- ifelse(home_proj_df$off==team, team_data$off_rating, home_proj_df$off_rating)
    home_proj_df$def_rating <- ifelse(home_proj_df$def==team, team_data$def_rating, home_proj_df$def_rating)
  }
  
  return (home_proj_df)
}
