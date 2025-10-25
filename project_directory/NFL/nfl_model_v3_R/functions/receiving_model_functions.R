build_initial_rec_train_frame <- function(pfr_rec_df) {
  train_rec_df <- pfr_rec_df
  train_rec_df <- train_rec_df[!(train_rec_df$tm_pass_attempts==0),]
  return (train_rec_df)
}

remove_player_history <- function(train_rec_df) {
  #Arizona
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Marvin Harrison Jr.' & train_rec_df$season==2024 & train_rec_df$week %in% c(1,5,6,7)),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Zay Jones' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name == 'Trey McBride' & (train_rec_df$season==2022 | (train_rec_df$season==2023 & train_rec_df$week<=7))), ]
  #Atlanta
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Drake London' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Darnell Mooney' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Ray-Ray McCloud' & train_rec_df$season<2024),]
  #Baltimore
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Derrick Henry' & (train_rec_df$season == 2022 | (train_rec_df$season==2023 & train_rec_df$week<=12))),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Rashod Bateman' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='DeAndre Hopkins' & train_rec_df$season<2024),]
  #Buffalo
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Khalil Shakir' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Keon Coleman' & train_rec_df$season==2024 & train_rec_df$week %in% c(2,16,17)),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Curtis Samuel' & train_rec_df$season<2024),]
  #Carolina
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Xavier Legette' & train_rec_df$season==2024 & train_rec_df$week %in% c(2,5)),]
  #Chicago
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Rome Odunze' & train_rec_df$season==2024 & train_rec_df$week %in% c(1,2,4)),]
  #Cincy
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Chase Brown' & train_rec_df$season<2024),]
  #Cleveland
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Jerry Jeudy' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Cedric Tillman' & train_rec_df$season<2024),]
  #Dallas
  #Denver
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Courtland Sutton' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Evan Engram' & train_rec_df$season==2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Marvin Mims' & train_rec_df$season<2024),]
  #Detroit
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Jameson Williams' & train_rec_df$season<2024),]
  #Green Bay
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Tucker Kraft' & train_rec_df$season<2024),]
  #Houston
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Nico Collins' & train_rec_df$season<2023),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Christian Kirk' & train_rec_df$season<2023),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Nick Chubb' & train_rec_df$season<2024),]
  #Indianapolis
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Josh Downs' & train_rec_df$season<2024),]
  #Jacksonville
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Brenton Strange' & train_rec_df$season<2024 & train_rec_df$week %in% c(1,7,9)),]
  #Kansas City
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Xavier Worthy' & train_rec_df$season==2024 & train_rec_df$week %in% c(2,3,4,5)),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Travis Kelce' & train_rec_df$season<2023),]
  #Los Angeles Chargers
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Quentin Johnston' & train_rec_df$season<2024),]
  #Los Angeles Rams
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Puka Nacua' & train_rec_df$season==2023 & train_rec_df$week %in% c(6,7,8,9)),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Davante Adams' & (train_rec_df$season<2023 | (train_rec_df$season==2023 & train_rec_df$week<=8))),]
  #Las Vegas Raiders
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Brock Bowers' & train_rec_df$season==2024 & train_rec_df$week %in% c(1,4)),]
  #Miami
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Tyreek Hill' & (train_rec_df$season<2023 | (train_rec_df$season==2023 & train_rec_df$week<=8))),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Jaylen Waddle' & train_rec_df$season==2024 & train_rec_df$week %in% c(7,9,15)),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Nick Westbrook-Ikhine' & train_rec_df$season==2024),]
  #Minnesota
  train_rush_df <- train_rush_df[!(train_rush_df$player_name=='Aaron Jones' & train_rush_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Ty Chandler' & train_rec_df$season<2024),]
  #New England
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Stefon Diggs' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Demario Douglas' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Hunter Henry' & train_rec_df$season<2023),]
  #New Orleans
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Brandin Cooks' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Cedrick Wilson Jr.' & train_rec_df$season<2024),]
  #New York Giants
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=="Wan'Dale Robinson" & train_rec_df$season<2023),]
  #New York Jets
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Garrett Wilson' & train_rec_df$season==2022 & train_rec_df$week %in% c(4,5,6,7,10)),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=="Allen Lazard" & (train_rec_df$season==2022|train_rec_df$season==2024)),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Josh Reynolds' & train_rec_df$season<2024),]
  #Philadelphia
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Saquon Barkley' & (train_rec_df$season == 2022 | (train_rec_df$season==2023 & train_rec_df$week<=12))),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Jahan Dotson' & train_rec_df$season<2023),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Dallas Goedert' & train_rec_df$season==2024 & train_rec_df$week==5),]
  #Pittsburgh
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Jonnu Smith' & train_rec_df$season<2023),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Calvin Austin III' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Robert Woods' & train_rec_df$season<2024),]
  #Seattle
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Jaxon Smith-Njigba' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Jaxon Smith-Njigba' & train_rec_df$season==2024 & train_rec_df$week %in% c(1,3,17,18)),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Cooper Kupp' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Marquez Valdes-Scantling' & train_rec_df$season==2024 & train_rec_df$week<8),]
  #San Francisco
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Jauan Jennings' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Ricky Pearsall' & train_rec_df$season==2024 & train_rec_df$week %in% c(7,11,12,13,14,15)),]
  #Tampa Bay
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Cade Otton' & train_rec_df$season<2024),]
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Jalen McMillan' & train_rec_df$season==2024 & train_rec_df$week %in% c(17,18)),]
  #Tennessee
  #Washington
  train_rec_df <- train_rec_df[!(train_rec_df$player_name=='Austin Ekeler' & train_rec_df$season<2024),]
  
  return (train_rec_df)
}

create_usage_metrics <- function(train_rec_df){
  train_rec_df$tgt_share <- round(as.numeric(train_rec_df$targets)/as.numeric(train_rec_df$tm_pass_attempts), 3)
  train_rec_df$tgt_conv <- round(as.numeric(train_rec_df$receptions)/as.numeric(train_rec_df$targets), 3)
  train_rec_df$yards_per_rec <- ifelse(train_rec_df$receptions==0, as.numeric(0.00),round(as.numeric(train_rec_df$receiving_yards)/as.numeric(train_rec_df$receptions), 2))
  train_rec_df$rec_td_share <- ifelse(train_rec_df$tm_pass_touchdowns==0, as.numeric(0.000), round(as.numeric(train_rec_df$receiving_touchdowns)/as.numeric(train_rec_df$tm_pass_touchdowns), 3))
  return (train_rec_df)
}

build_test_set_home <- function(proj_df){
  test_rec_home <- subset(proj_df, select = c("key","home","away"))
  colnames(test_rec_home) <- c("key","team","opp")
  test_rec_home$off_rating <- 0.0
  test_rec_home$def_rating <- 0.0
  for (team in model_params$nfl_teams) {
    team_rating <- current_ratings[(current_ratings$team==team),]
    test_rec_home$off_rating <- ifelse(test_rec_home$team==team, team_rating$off_rating, test_rec_home$off_rating)
    test_rec_home$def_rating <- ifelse(test_rec_home$opp==team, team_rating$def_rating, test_rec_home$def_rating)
  }
  return (test_rec_home)
}

build_test_set_away <- function(proj_df){
  test_rec_away <- subset(proj_df, select = c("key","away","home"))
  colnames(test_rec_away) <- c("key","team","opp")
  test_rec_away$off_rating <- 0.0
  test_rec_away$def_rating <- 0.0
  for (team in model_params$nfl_teams) {
    team_rating <- current_ratings[(current_ratings$team==team),]
    test_rec_away$off_rating <- ifelse(test_rec_away$team==team, team_rating$off_rating, test_rec_away$off_rating)
    test_rec_away$def_rating <- ifelse(test_rec_away$opp==team, team_rating$def_rating, test_rec_away$def_rating)
  }
  return (test_rec_away)
}

run_pass_catcher_projections <- function(receiver_name, receiver_stats_name, position, weekly_matchup_test_values, target_share_model, target_conversion_model, yards_per_reception_model, td_share_model){
  rec_test <- weekly_matchup_test_values
  rec_test$player_name <- receiver_stats_name
  rec_test$pos <- position
  
  target_share_model_output <- predict(target_share_model, rec_test)
  target_conversion_model_output <- predict(target_conversion_model, rec_test)
  yards_per_reception_model_model_output <- predict(yards_per_reception_model, rec_test)
  td_share_model_output <- predict(td_share_model, rec_test)
  
  rec_test$tgt_share <- round(target_share_model_output[1], 3)
  rec_test$tgt_conv_rate <- round(target_conversion_model_output[1], 3)
  rec_test$yards_per_rec <- round(yards_per_reception_model_model_output[1], 3)
  rec_test$rec_td_share <- round(td_share_model_output[1], 3)
  
  rec_test$player_name <- receiver_name
  
  return (rec_test)
}



