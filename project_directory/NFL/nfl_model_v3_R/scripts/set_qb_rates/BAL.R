###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'BAL'
qb <- ifelse(impact_players[['bal_lamar_jackson']]==1,'Lamar Jackson','Cooper Rush')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['bal_lamar_jackson']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Lamar Jackson', stat_qb_name = 'Lamar Jackson', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Cooper Rush', stat_qb_name = 'Cooper Rush', home_away = TRUE)
}

rm(team, qb)
#####################################################################