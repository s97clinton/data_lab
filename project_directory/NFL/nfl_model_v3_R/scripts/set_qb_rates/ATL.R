###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'ATL'
qb <- ifelse(impact_players[['atl_michael_penix']]==1,'Michael Penix','Kirk Cousins')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['atl_michael_penix']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Michael Penix', stat_qb_name = 'Michael Penix', home_away = FALSE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Kirk Cousins', stat_qb_name = 'Kirk Cousins', home_away = TRUE)
}

rm(team, qb)
#####################################################################