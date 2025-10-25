###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'NYG'
qb <- ifelse(impact_players[['nyg_russell_wilson']]==1,'Russell Wilson','Jameis Winston')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['nyg_russell_wilson']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Russell Wilson', stat_qb_name = 'Russell Wilson', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Jameis Winston', stat_qb_name = 'Jameis Winston', home_away = TRUE)
}

rm(team, qb)
#####################################################################