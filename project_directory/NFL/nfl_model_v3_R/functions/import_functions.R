source("functions/credentials.R")
source("functions/utils.R")

#' Set NFL model parameters
#'
#' This function defines parameters for an NFL model based on the provided season
#' and week range, including seasons, weeks, teams, and projection weeks.
#'
#' @param season Numeric. The current NFL season year (e.g., 2025).
#' @param start_week Numeric. The starting week for projections.
#' @param end_week Numeric. The ending week for projections.
#' @return A named list containing:
#' \itemize{
#'   \item current_season: The input season year.
#'   \item start_season: The season 3 years prior to the current season.
#'   \item nfl_seasons: A sequence of seasons from start_season to current_season.
#'   \item nfl_weeks: A sequence of weeks from 1 to 22.
#'   \item nfl_teams: A character vector of NFL team abbreviations.
#'   \item projection_weeks: A sequence of weeks from start_week to end_week.
#'   \item game_wk: The first week in projection_weeks.
#' }
#' @examples
#' \dontrun{
#' params <- set_model_parameters(2025, 1, 5)
#' print(params$current_season)
#' print(params$nfl_teams)
#' }
#' @export
set_model_parameters <- function(season, start_week, end_week){
  current_season <- season
  start_season <- season - 3
  nfl_seasons <- seq(start_season, current_season)
  nfl_weeks <- seq(1, 22)
  nfl_teams <- list('ARI','ATL','BAL','BUF','CAR','CHI','CIN','CLE','DAL','DEN','DET','GB','HOU','IND','JAX','KC','LAC','LAR','LVR','MIA','MIN','NE','NO','NYG','NYJ','PHI','PIT','SEA','SF','TB','TEN','WSH')
  projection_weeks <- seq(start_week, end_week)
  game_wk <- projection_weeks[1]
  injuries <- "yes"
  fantasy_player_projection <- 0
  return(list(current_season=current_season, start_season=start_season, nfl_seasons=nfl_seasons, 
              nfl_weeks=nfl_weeks, nfl_teams=nfl_teams, projection_weeks=projection_weeks, game_wk=game_wk, 
              injuries=injuries, fantasy_player_projection=fantasy_player_projection))
}


#' Import NFL schedule from a CSV file
#'
#' This function reads an NFL schedule CSV file for a specified season and returns
#' a data frame with lowercase column names.
#'
#' @param season Numeric. The NFL season year (e.g., 2025).
#' @return A data frame containing the NFL schedule with lowercase column names.
#' @examples
#' \dontrun{
#' schedule <- import_schedule(2025)
#' head(schedule)
#' }
#' @export
import_schedule <- function(season) {
  schedule_path <- paste0("data_files/schedules/nfl_schedule_",season,".csv")
  nfl_schedule <- read.csv(schedule_path)
  names(nfl_schedule) <- tolower(names(nfl_schedule))
  return(nfl_schedule)
}

#' Import Historic DVOA Data from a CSV file
#'
#' This function reads an Historic DVOA Data CSV file and returns
#' a data frame with lowercase column names.
#'
#' @param start_season Numeric. First Year of Data to Pull.
#' @param current_season Numeric. Last Year of Data to Pull.
#' @return A data frame containing the Historic DVOA Data with lowercase column names.
#' @examples
#' \dontrun{
#' historic_dvoa <- import_historic_dvoa(2022, 2025)
#' head(historic_dvoa)
#' }
#' @export
import_historic_dvoa <- function(start_season, current_season) {
  historic_dvoa <- read.csv("data_files/dvoa_historic/historic_dvoa.csv")
  names(historic_dvoa) <- tolower(names(historic_dvoa))
  historic_dvoa$team <- ifelse(historic_dvoa$team %in% c("LV", "OAK"), "LVR", historic_dvoa$team)
  historic_dvoa$team <- ifelse(historic_dvoa$team == 'WAS', "WSH", historic_dvoa$team)
  historic_dvoa$offense_dvoa <- as.numeric(gsub("%", "", historic_dvoa$offense_dvoa)) / 100
  historic_dvoa$defense_dvoa <- as.numeric(gsub("%", "", historic_dvoa$defense_dvoa)) / 100
  historic_dvoa <- subset(historic_dvoa, select = -c(offense_dvoa_rank, defense_dvoa_rank))
  colnames(historic_dvoa) <- c('season', 'team', 'off_rating', 'def_rating')
  historic_dvoa <- subset(historic_dvoa, season >= start_season & season <= current_season)
  return(historic_dvoa)
}

#' Import Coaching Data from a CSV file
#'
#' This function reads an Historic Coaching Data CSV file and returns
#' a data frame with lowercase column names.
#'
#' @param start_season Numeric. First Year of Data to Pull.
#' @param current_season Numeric. Last Year of Data to Pull.
#' @return A data frame containing the Historic Coaching Data.
#' @examples
#' \dontrun{
#' nfl_coaches <- import_nfl_coaches(2022, 2025)
#' head(nfl_coaches)
#' }
#' @export
import_nfl_coaches <- function(start_season, current_season) {
  nfl_coaches <- read.csv("data_files/coach_qb_table/nfl_coach_qb_table.csv")
  nfl_coaches <- subset(nfl_coaches, season >= start_season & season <= current_season)
  return(nfl_coaches)
}

#' Import pfr_game_basic from MySQL database
#'
#' This function connects to a MySQL database and returns
#' a data frame from the table pfr_game_basic.
#'
#' @param start_season Numeric. First Year of Data to Pull.
#' @param current_season Numeric. Last Year of Data to Pull.
#' @return A data frame containing the pfr_game_basic data.
#' @examples
#' \dontrun{
#' pfr_game_basic <- import_pfr_game_basic(2022, 2025)
#' head(pfr_game_basic)
#' }
#' @export
import_pfr_game_basic <- function(start_season, current_season) {
  nfl_db = connect_my_sql_db(user, password)
  rm <- dbSendQuery(nfl_db, paste("SELECT *
                                FROM nfl.pfr_game_basic
                                WHERE nfl.pfr_game_basic.season>=", start_season,"
                                AND nfl.pfr_game_basic.season<=", current_season, ";", sep=""))
  pfr_game_basic <- fetch(rm, n=-1)
  dbClearResult(rm)
  dbDisconnect(nfl_db)
  return(pfr_game_basic)
}

#' Import pfr_team_stats from MySQL database
#'
#' This function connects to a MySQL database and returns
#' a data frame from the table pfr_team_stats
#'
#' @param game_ids List. Game IDs to query in database.
#' @return A data frame containing the pfr_team_stats data.
#' @examples
#' \dontrun{
#' pfr_team_stats <- import_pfr_team_stats(game_ids)
#' head(pfr_team_stats)
#' }
#' @export
import_pfr_team_stats <- function(game_ids) {
  nfl_db = connect_my_sql_db(user, password)
  game_ids_string <- paste("'", game_ids, "'", sep = "", collapse = ",")
  query <- paste("SELECT *
                  FROM nfl.pfr_team_stats
                  WHERE nfl.pfr_team_stats.game_id IN (", game_ids_string, ");", sep = "")
  rm <- dbSendQuery(nfl_db, query)
  pfr_team_stats <- fetch(rm, n=-1)
  dbClearResult(rm)
  dbDisconnect(nfl_db)
  return(pfr_team_stats)
}

#' Import pfr_passing_base from MySQL database
#'
#' This function connects to a MySQL database and returns
#' a data frame from the table pfr_passing_base
#'
#' @param game_ids List. Game IDs to query in database.
#' @return A data frame containing the pfr_passing_base data.
#' @examples
#' \dontrun{
#' pfr_pass_stats <- import_pfr_pass_stats(game_ids)
#' head(pfr_pass_stats)
#' }
#' @export
import_pfr_pass_stats <- function(game_ids) {
  nfl_db = connect_my_sql_db(user, password)
  game_ids_string <- paste("'", game_ids, "'", sep = "", collapse = ",")
  query <- paste("SELECT t.*, b.season, b.week, b.opp, b.venue
                  FROM nfl.pfr_passing_base t
                  JOIN nfl.pfr_game_basic b ON t.game_id = b.game_id AND t.team = b.team
                  WHERE t.game_id IN (", game_ids_string, ");", sep = "")
  rm <- dbSendQuery(nfl_db, query)
  pfr_pass_stats <- fetch(rm, n=-1)
  dbClearResult(rm)
  dbDisconnect(nfl_db)
  return(pfr_pass_stats)
}

#' Import pfr_rushing_base from MySQL database
#'
#' This function connects to a MySQL database and returns
#' a data frame from the table pfr_rushing_base
#'
#' @param game_ids List. Game IDs to query in database.
#' @return A data frame containing the pfr_rushing_base data.
#' @examples
#' \dontrun{
#' pfr_rush_stats <- import_pfr_rush_stats(game_ids)
#' head(pfr_rush_stats)
#' }
#' @export
import_pfr_rush_stats <- function(game_ids) {
  nfl_db = connect_my_sql_db(user, password)
  game_ids_string <- paste("'", game_ids, "'", sep = "", collapse = ",")
  query <- paste("SELECT t.*, b.season, b.week, b.opp, b.venue
                  FROM nfl.pfr_rushing_base t
                  JOIN nfl.pfr_game_basic b ON t.game_id = b.game_id AND t.team = b.team
                  WHERE t.game_id IN (", game_ids_string, ");", sep = "")
  rm <- dbSendQuery(nfl_db, query)
  pfr_rush_stats <- fetch(rm, n=-1)
  dbClearResult(rm)
  dbDisconnect(nfl_db)
  return(pfr_rush_stats)
}

#' Import pfr_receiving_base from MySQL database
#'
#' This function connects to a MySQL database and returns
#' a data frame from the table pfr_receiving_base
#'
#' @param game_ids List. Game IDs to query in database.
#' @return A data frame containing the pfr_receiving_base data.
#' @examples
#' \dontrun{
#' pfr_rec_stats <- import_pfr_rec_stats(game_ids)
#' head(pfr_rec_stats)
#' }
#' @export
import_pfr_rec_stats <- function(game_ids) {
  nfl_db = connect_my_sql_db(user, password)
  game_ids_string <- paste("'", game_ids, "'", sep = "", collapse = ",")
  query <- paste("SELECT t.*, b.season, b.week, b.opp, b.venue
                  FROM nfl.pfr_receiving_base t
                  JOIN nfl.pfr_game_basic b ON t.game_id = b.game_id AND t.team = b.team
                  WHERE t.game_id IN (", game_ids_string, ");", sep = "")
  rm <- dbSendQuery(nfl_db, query)
  pfr_rec_stats <- fetch(rm, n=-1)
  dbClearResult(rm)
  dbDisconnect(nfl_db)
  return(pfr_rec_stats)
}

#' Import pfr_drive_info from MySQL database
#'
#' This function connects to a MySQL database and returns
#' a data frame from the table pfr_drive_info
#'
#' @param start_season Numeric. First Year of Data to Pull.
#' @param current_season Numeric. Last Year of Data to Pull.
#' @return A data frame containing the pfr_drive_info data.
#' @examples
#' \dontrun{
#' pfr_drive_data <- import_pfr_drive_data(2022, 2025)
#' head(pfr_drive_data)
#' }
#' @export
import_pfr_drive_data <- function(start_season, current_season) {
  nfl_db = connect_my_sql_db(user, password)
  rm <- dbSendQuery(nfl_db, paste("SELECT *
                                FROM nfl.pfr_drive_info
                                WHERE nfl.pfr_drive_info.season>=", start_season,"
                                AND nfl.pfr_drive_info.season<=", current_season, ";", sep=""))
  pfr_drive_data <- fetch(rm, n=-1)
  pfr_drive_data$drive_start_comparison_time <- strtoi(as.difftime(pfr_drive_data$drive_start_time, format = "%M:%S", units = "secs"))
  pfr_drive_data$drive_length_comparison_time <- strtoi(as.difftime(pfr_drive_data$drive_time, format = "%M:%S", units = "secs"))
  pfr_drive_data$qtr <- ifelse((pfr_drive_data$qtr==1|pfr_drive_data$qtr==3)&(pfr_drive_data$drive_length_comparison_time>pfr_drive_data$drive_start_comparison_time),(as.numeric(pfr_drive_data$qtr)+1),as.numeric(pfr_drive_data$qtr))
  pfr_drive_data <- subset(pfr_drive_data, select = -c(drive_start_comparison_time, drive_length_comparison_time))
  
  dbClearResult(rm)
  dbDisconnect(nfl_db)
  return(pfr_drive_data)
}


