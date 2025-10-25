###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'MIN'
qb <- ifelse(impact_players[['min_jj_mccarthy']]==1,'J.J. McCarthy','Carson Wentz')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['min_jj_mccarthy']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'J.J. McCarthy', stat_qb_name = 'Jared Goff', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Carson Wentz', stat_qb_name = 'Carson Wentz', home_away = TRUE)
}

rm(team, qb)
#####################################################################

