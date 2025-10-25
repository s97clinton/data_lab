set_third_down_rates <- function(proj_df, pfr_team_stats) {
  
  team_third_down_df <- pfr_team_stats
  team_third_down_df <- team_third_down_df[complete.cases(team_third_down_df[, c("third_down_conversions", "third_down_attempts")]), ]
  
  proj_df$away_off_third_down_perc <- 0.0
  proj_df$home_off_third_down_perc <- 0.0
  proj_df$away_def_third_down_perc <- 0.0
  proj_df$home_def_third_down_perc <- 0.0
  
  for (team in model_params$nfl_teams){
    team_third_dn_road_off <- team_third_down_df[(team_third_down_df$venue=='Away' & team_third_down_df$team==team),]
    team_third_dn_road_def <- team_third_down_df[(team_third_down_df$venue=='Away' & team_third_down_df$opp==team),]
    team_third_dn_home_off <- team_third_down_df[(team_third_down_df$venue=='Home' & team_third_down_df$team==team),]
    team_third_dn_home_def <- team_third_down_df[(team_third_down_df$venue=='Home' & team_third_down_df$opp==team),]
    
    team_third_dn_road_off_rate <- sum(as.numeric(team_third_dn_road_off$third_down_conversions))/sum(as.numeric(team_third_dn_road_off$third_down_attempts))
    team_third_dn_road_def_rate <- 1 - sum(as.numeric(team_third_dn_road_def$third_down_conversions))/sum(as.numeric(team_third_dn_road_def$third_down_attempts))
    team_third_dn_home_off_rate <- sum(as.numeric(team_third_dn_home_off$third_down_conversions))/sum(as.numeric(team_third_dn_home_off$third_down_attempts))
    team_third_dn_home_def_rate <- 1 - sum(as.numeric(team_third_dn_home_def$third_down_conversions))/sum(as.numeric(team_third_dn_home_def$third_down_attempts))
    
    proj_df$away_off_third_down_perc <- ifelse(proj_df$away==team,team_third_dn_road_off_rate,proj_df$away_off_third_down_perc)
    proj_df$away_def_third_down_perc <- ifelse(proj_df$away==team,team_third_dn_road_def_rate,proj_df$away_def_third_down_perc)
    proj_df$home_off_third_down_perc <- ifelse(proj_df$home==team,team_third_dn_home_off_rate,proj_df$home_off_third_down_perc)
    proj_df$home_def_third_down_perc <- ifelse(proj_df$home==team,team_third_dn_home_def_rate,proj_df$home_def_third_down_perc)
  }
  
  proj_df$away_off_third_down_perc <- round(as.numeric(proj_df$away_off_third_down_perc),2)
  proj_df$away_def_third_down_perc <- round(as.numeric(proj_df$away_def_third_down_perc),2)
  proj_df$home_off_third_down_perc <- round(as.numeric(proj_df$home_off_third_down_perc),2)
  proj_df$home_def_third_down_perc <- round(as.numeric(proj_df$home_def_third_down_perc),2)
  
  return (proj_df)
}