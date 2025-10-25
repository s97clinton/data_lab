###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'TB'
qb <- ifelse(impact_players[['tb_baker_mayfield']]==1,'Baker Mayfield','Teddy Bridgewater')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['tb_baker_mayfield']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Baker Mayfield', stat_qb_name = 'Baker Mayfield', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Teddy Bridgewater', stat_qb_name = 'Teddy Bridgewater', home_away = FALSE)
}

rm(team, qb)
#####################################################################