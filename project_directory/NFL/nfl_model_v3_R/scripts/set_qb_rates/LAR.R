###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'LAR'
qb <- ifelse(impact_players[['lar_matt_stafford']]==1,'Matthew Stafford','Jimmy Garoppolo')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['lar_matt_stafford']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Matthew Stafford', stat_qb_name = 'Matthew Stafford', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Jimmy Garoppolo', stat_qb_name = 'Jimmy Garoppolo', home_away = TRUE)
}

rm(team, qb)
#####################################################################