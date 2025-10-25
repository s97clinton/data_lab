###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'TEN'
qb <- ifelse(impact_players[['ten_cam_ward']]==1,'Cam Ward','Brandon Allen')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['ten_cam_ward']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Cam Ward', stat_qb_name = 'Kyler Murray', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Brandon Allen', stat_qb_name = 'Brandon Allen', home_away = TRUE)
}

rm(team, qb)
#####################################################################