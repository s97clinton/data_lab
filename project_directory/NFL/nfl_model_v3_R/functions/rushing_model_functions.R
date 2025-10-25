build_initial_rush_train_frame <- function(pfr_rush_df) {
  train_rush_df <- pfr_rush_df
  train_rush_df <- train_rush_df[!(train_rush_df$tm_rush_attempts==0),]
  return (train_rush_df)
}

remove_player_history <- function(train_rush_df) {
  #Arizona
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Trey Benson' & train_rush_df$season==2024 & train_rush_df$week %in% c(3,7,8)),]
  #Atlanta
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Bijan Robinson' & train_rush_df$season<2024),]
  #Baltimore
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Derrick Henry' & (train_rush_df$season == 2022 | (train_rush_df$season==2023 & train_rush_df$week %in% c(6,13,16,18)))),]
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Lamar Jackson' & train_rush_df$season<2023),]
  #Buffalo
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Josh Allen' & train_rush_df$season<2023),]
  #Carolina
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Chuba Hubbard' & train_rush_df$season<2024),]
  #Chicago
  #Cincy
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Chase Brown' & train_rush_df$season<2024 | (train_rush_df$season==2024 & train_rush_df$week<=3)),]
  #Cleveland
  #Dallas
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Miles Sanders' & train_rush_df$season<2023),]
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Dak Prescott' & train_rush_df$season<2024),]
  #Denver
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='J.K. Dobbins' & train_rush_df$season<2023),]
  #Detroit
  #Green Bay
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Josh Jacobs' & train_rush_df$season<2023),]
  #Houston
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Joe Mixon' & train_rush_df$season<2023),]
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Nick Chubb' & train_rush_df$season<2024),]
  #Indianapolis
  #Jacksonville
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Tank Bigsby' & train_rush_df$season<2024),]
  #Kansas City
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Isiah Pacheco' & train_rush_df$season==2024 & train_rush_df$week>18),]
  #Los Angeles Chargers
  #Los Angeles Rams
  #Las Vegas Raiders
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Raheem Mostert' & train_rush_df$season==2023),]
  #Miami
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Alexander Mattison' & ((train_rush_df$season==2022 & train_rush_df$week==18) | train_rush_df$season == 2023 | train_rush_df$season==2024)),]
  #Minnesota
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Aaron Jones' & train_rush_df$season<2024),]
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Jordan Mason' & train_rush_df$season<2024),]
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Ty Chandler' & train_rush_df$season<2024),]
  #New England
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Drake Maye' & train_rush_df$season==2024 & train_rush_df$week>16),]
  #New Orleans
  #New York Giants
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Devin Singletary' & train_rush_df$season<2024),]
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Russell Wilson' & train_rush_df$season<2024),]
  #New York Jets
  #Philadelphia
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Saquon Barkley' & (train_rush_df$season == 2022 | (train_rush_df$season==2023 & train_rush_df$week<=12))),]
  #Pittsburgh
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Jaylen Warren' & train_rush_df$season<2023),]
  #Seattle
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Zach Charbonnet' & train_rush_df$season<2024),]
  #San Francisco
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Christian McCaffrey' & train_rush_df$season==2023 & train_rush_df$week<12),]
  #Tampa Bay
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Rachaad White' & train_rush_df$season<2024),]
  #Tennessee
  #Washington
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Austin Ekeler' & train_rush_df$season<2024),]
  
  return (train_rush_df)
}

create_usage_metrics <- function(train_rush_df){
  train_rush_df$carry_perc <- round(as.numeric(train_rush_df$rush_attempts)/as.numeric(train_rush_df$tm_rush_attempts), 3)
  train_rush_df$yards_per_carry <- round(as.numeric(train_rush_df$rushing_yards)/as.numeric(train_rush_df$rush_attempts), 2)
  train_rush_df$rush_td_share <- ifelse(train_rush_df$tm_rush_touchdowns==0, as.numeric(0.000), round(as.numeric(train_rush_df$rushing_touchdowns)/as.numeric(train_rush_df$tm_rush_touchdowns), 3))
  return (train_rush_df)
}

build_test_set_home <- function(proj_df){
  test_rush_home <- subset(proj_df, select = c("key","home","away"))
  colnames(test_rush_home) <- c("key","team","opp")
  test_rush_home$off_rating <- 0.0
  test_rush_home$def_rating <- 0.0
  for (team in model_params$nfl_teams) {
    team_rating <- current_ratings[(current_ratings$team==team),]
    test_rush_home$off_rating <- ifelse(test_rush_home$team==team, team_rating$off_rating, test_rush_home$off_rating)
    test_rush_home$def_rating <- ifelse(test_rush_home$opp==team, team_rating$def_rating, test_rush_home$def_rating)
  }
  return (test_rush_home)
}

build_test_set_away <- function(proj_df){
  test_rush_away <- subset(proj_df, select = c("key","away","home"))
  colnames(test_rush_away) <- c("key","team","opp")
  test_rush_away$off_rating <- 0.0
  test_rush_away$def_rating <- 0.0
  for (team in model_params$nfl_teams) {
    team_rating <- current_ratings[(current_ratings$team==team),]
    test_rush_away$off_rating <- ifelse(test_rush_away$team==team, team_rating$off_rating, test_rush_away$off_rating)
    test_rush_away$def_rating <- ifelse(test_rush_away$opp==team, team_rating$def_rating, test_rush_away$def_rating)
  }
  return (test_rush_away)
}

run_ballcarrier_projections <- function(rusher_name, rusher_stats_name, position, weekly_matchup_test_values, carry_share_model, yards_per_carry_model, td_share_model){
  rush_test <- weekly_matchup_test_values
  rush_test$player_name <- rusher_stats_name
  rush_test$pos <- position
  
  carry_share_model_output <- predict(carry_share_model, rush_test)
  yards_per_carry_model_output <- predict(yards_per_carry_model, rush_test)
  td_share_model_output <- predict(td_share_model, rush_test)
  
  rush_test$carry_share <- round(carry_share_model_output[1], 3)
  rush_test$yards_per_carry <- round(yards_per_carry_model_output[1], 3)
  rush_test$rush_td_share <- round(td_share_model_output[1], 3)
  
  rush_test$player_name <- rusher_name
  
  return (rush_test)
}

