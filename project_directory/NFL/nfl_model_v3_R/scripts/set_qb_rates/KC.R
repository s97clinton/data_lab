###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'KC'
qb <- ifelse(impact_players[['kc_pat_mahomes']]==1,'Patrick Mahomes','Gardner Minshew')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['kc_pat_mahomes']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Patrick Mahomes', stat_qb_name = 'Patrick Mahomes', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Gardner Minshew', stat_qb_name = 'Gardner Minshew', home_away = TRUE)
}

rm(team, qb)
#####################################################################