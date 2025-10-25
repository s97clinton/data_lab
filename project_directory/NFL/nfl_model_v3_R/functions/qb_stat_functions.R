set_team_qb <- function(proj_df, team, qb) {
  proj_df$away_qb <- ifelse(proj_df$away==team, qb, proj_df$away_qb)
  proj_df$home_qb <- ifelse(proj_df$home==team, qb, proj_df$home_qb)
  return(proj_df)
}

set_qb_int_sack_rates <- function(proj_df, pfr_pass_df, qb_name, stat_qb_name, home_away) {
  
  pfr_pass_df <- pfr_pass_df[!(pfr_pass_df$player_name=='Josh Allen' & pfr_pass_df$season<2024),]
  
  if (home_away) {
    away_qb_df <- pfr_pass_df[(pfr_pass_df$player_name==stat_qb_name & pfr_pass_df$venue=='Away'),]
    home_qb_df <- pfr_pass_df[(pfr_pass_df$player_name==stat_qb_name & pfr_pass_df$venue=='Home'),]
  } else {
    away_qb_df <- pfr_pass_df[(pfr_pass_df$player_name==stat_qb_name),]
    home_qb_df <- pfr_pass_df[(pfr_pass_df$player_name==stat_qb_name),]
  }  
  
  away_int_rate <- round(((sum(as.numeric(away_qb_df$interceptions)))/(sum(as.numeric(away_qb_df$pass_attempts)))),3)
  home_int_rate <- round(((sum(as.numeric(home_qb_df$interceptions)))/(sum(as.numeric(home_qb_df$pass_attempts)))),3)
  away_sack_rate <- round(((sum(as.numeric(away_qb_df$sacks)))/(sum(as.numeric(away_qb_df$pass_attempts)))),3)
  home_sack_rate <- round(((sum(as.numeric(home_qb_df$sacks)))/(sum(as.numeric(home_qb_df$pass_attempts)))),3)
  
  proj_df$away_qb_int_rate <- ifelse(proj_df$away_qb==qb_name, away_int_rate, proj_df$away_qb_int_rate)
  proj_df$home_qb_int_rate <- ifelse(proj_df$home_qb==qb_name, home_int_rate, proj_df$home_qb_int_rate)
  proj_df$away_qb_sack_rate <- ifelse(proj_df$away_qb==qb_name, away_sack_rate, proj_df$away_qb_sack_rate)
  proj_df$home_qb_sack_rate <- ifelse(proj_df$home_qb==qb_name, home_sack_rate, proj_df$home_qb_sack_rate)
  
  return(proj_df)
}