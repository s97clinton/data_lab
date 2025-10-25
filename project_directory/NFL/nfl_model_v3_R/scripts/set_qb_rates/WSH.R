###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'WSH'
qb <- ifelse(impact_players[['wsh_jayden_daniels']]==1,'Jayden Daniels','Marcus Mariota')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['wsh_jayden_daniels']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Jayden Daniels', stat_qb_name = 'Jayden Daniels', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Marcus Mariota', stat_qb_name = 'Marcus Mariota', home_away = TRUE)
}

rm(team, qb)
#####################################################################