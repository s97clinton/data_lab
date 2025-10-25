###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'MIA'
qb <- ifelse(impact_players[['mia_tua_tagovailoa']]==1,'Tua Tagovailoa','Zach Wilson')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['mia_tua_tagovailoa']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Tua Tagovailoa', stat_qb_name = 'Tua Tagovailoa', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Zach Wilson', stat_qb_name = 'Zach Wilson', home_away = TRUE)
}

rm(team, qb)
#####################################################################