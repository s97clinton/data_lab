create_factor_outcomes <- function(drive_outcome_train_df) {
  drive_outcome_factors_train_df <- drive_outcome_train_df

  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Touchdown','touchdown','')
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Blocked FG','fg_fail',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Blocked FG, Downs','fg_fail',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Missed FG','fg_fail',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Field Goal','fg',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Blocked Punt','punt',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Blocked Punt, Downs','punt',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Blocked Punt, Safety','punt',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Punt','punt',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Fumble, Safety','safety',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Safety','safety',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Fumble','fumble',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Downs','downs',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='Interception','interception',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='End of Game','end_game',drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- ifelse(drive_outcome_factors_train_df$drive_result=='End of Half','end_half',drive_outcome_factors_train_df$drive_result_grouped)
  
  drive_outcome_factors_train_df$drive_result_grouped <- as.factor(drive_outcome_factors_train_df$drive_result_grouped)
  drive_outcome_factors_train_df$drive_result_grouped <- relevel(drive_outcome_factors_train_df$drive_result_grouped, ref = "touchdown")
  
  drive_outcome_factors_train_df$qtr <- as.factor(drive_outcome_factors_train_df$qtr)
  drive_outcome_factors_train_df$venue <- as.factor(drive_outcome_factors_train_df$venue)
  drive_outcome_factors_train_df$off_rating <- as.numeric(drive_outcome_factors_train_df$off_rating)
  drive_outcome_factors_train_df$def_rating <- as.numeric(drive_outcome_factors_train_df$def_rating)
  
  return (drive_outcome_factors_train_df)
}


create_numeric_outcomes <- function(drive_outcome_train_df) {
  drive_outcome_numeric_train_df <- drive_outcome_train_df
  
  drive_outcome_numeric_train_df$drive_result_numeric <- as.numeric(0)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Touchdown',7,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Blocked FG',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Blocked FG, Downs',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Missed FG',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Field Goal',3,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Blocked Punt',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Blocked Punt, Downs',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Blocked Punt, Safety',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Punt',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Fumble, Safety',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Safety',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Fumble',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Downs',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='Interception',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='End of Game',0,drive_outcome_numeric_train_df$drive_result_numeric)
  drive_outcome_numeric_train_df$drive_result_numeric <- ifelse(drive_outcome_numeric_train_df$drive_result=='End of Half',0,drive_outcome_numeric_train_df$drive_result_numeric)
  
  drive_outcome_numeric_train_df$qtr <- as.factor(drive_outcome_numeric_train_df$qtr)
  drive_outcome_numeric_train_df$venue <- as.factor(drive_outcome_numeric_train_df$venue)
  drive_outcome_numeric_train_df$off_rating <- as.numeric(drive_outcome_numeric_train_df$off_rating)
  drive_outcome_numeric_train_df$def_rating <- as.numeric(drive_outcome_numeric_train_df$def_rating)
  
  return (drive_outcome_numeric_train_df)
}
