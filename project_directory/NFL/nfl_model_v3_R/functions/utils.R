library(dplyr)
library(RMySQL)

connect_my_sql_db <- function(user, password) {
  nfl_db = dbConnect(MySQL(), user=user, password=password, dbname='nfl')
  return(nfl_db)
}

create_qtr_multipliers <- function(drive_data) {
  drives_by_qtr <- drive_data %>% count(venue,qtr)
  drives_by_qtr <- drives_by_qtr[(as.numeric(drives_by_qtr$qtr)>=1 & as.numeric(drives_by_qtr$qtr)<=4),]
  drives_by_qtr_away <- drives_by_qtr[(drives_by_qtr$venue=='away'),]
  drives_by_qtr_home <- drives_by_qtr[(drives_by_qtr$venue=='home'),]
  drives_by_qtr_away$multiplier <- drives_by_qtr_away$n/(sum(drives_by_qtr_away$n))
  drives_by_qtr_home$multiplier <- drives_by_qtr_home$n/(sum(drives_by_qtr_home$n))
  away_multiplier_q1 <- as.numeric(drives_by_qtr_away[1,4])
  away_multiplier_q2 <- as.numeric(drives_by_qtr_away[2,4])
  away_multiplier_q3 <- as.numeric(drives_by_qtr_away[3,4])
  away_multiplier_q4 <- as.numeric(drives_by_qtr_away[4,4])
  home_multiplier_q1 <- as.numeric(drives_by_qtr_home[1,4])
  home_multiplier_q2 <- as.numeric(drives_by_qtr_home[2,4])
  home_multiplier_q3 <- as.numeric(drives_by_qtr_home[3,4])
  home_multiplier_q4 <- as.numeric(drives_by_qtr_home[4,4])
  return(list(away_multiplier_q1=away_multiplier_q1, away_multiplier_q2=away_multiplier_q2,
              away_multiplier_q3=away_multiplier_q3, away_multiplier_q4=away_multiplier_q4,
              home_multiplier_q1=home_multiplier_q1, home_multiplier_q2=home_multiplier_q2,
              home_multiplier_q3=home_multiplier_q3, home_multiplier_q4=home_multiplier_q4))
}

add_decay_dates <- function(df, lambda = 0.001){
  season_start_dates <- list( "2022" = as.Date("2022-09-11"), 
                              "2023" = as.Date("2023-09-10"), 
                              "2024" = as.Date("2024-09-08"), 
                              "2025" = as.Date("2025-09-07") )
  
  df$date <- mapply(function(season, week) {
    start_date <- season_start_dates[[as.character(season)]]
    if (is.null(start_date)) stop("Invalid season: ", season)
    start_date + (week - 1) * 7
  }, df$season, df$week, SIMPLIFY = TRUE)
  
  df$date <- as.Date(df$date, origin = "1970-01-01")
  current_date <- max(df$date, na.rm = TRUE)
  df$days_diff <- as.numeric(difftime(current_date, df$date, units = "days"))
  df$weight <- exp(-lambda * df$days_diff)
  
  return(df)
}
