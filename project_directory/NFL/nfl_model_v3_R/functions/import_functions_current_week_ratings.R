#' Import Current Ratings Data from a CSV file
#'
#' This function reads a Current Ratings Data CSV file and returns
#' a data frame with the columns renamed.
#'
#' @param current_season Numeric. Year of Data to Pull.
#' @param current_week Numeric. Week of Data to Pull.
#' @return A data frame containing the Current Rating with lowercase column names.
#' @examples
#' \dontrun{
#' current_dvoa <- import_current_ratings(2022, 2025)
#' head(historic_dvoa)
#' }
#' @export
import_current_ratings <- function(current_season, current_week) {
  # ratings_path <- paste0("data_files/current_ratings/", current_season,"/", current_season,"_SSRating_wk1.csv") #static path to run in offseason
  ratings_path <- paste0("data_files/current_ratings/", current_season,"/", current_season,"_SSRating_wk", current_week,".csv")
  current_ratings <- read.csv(ratings_path)
  current_ratings <- subset(current_ratings, select = c('Team', 'SS.OFF.DVOA', 'SS.DEF.DVOA'))
  colnames(current_ratings) <- c('team', 'off_rating', 'def_rating')
  current_ratings$season <- current_season
  
  return(current_ratings)
}