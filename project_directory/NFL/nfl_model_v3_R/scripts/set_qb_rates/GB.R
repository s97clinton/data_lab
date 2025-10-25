###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'GB'
qb <- ifelse(impact_players[['gb_jordan_love']]==1,'Jordan Love','Malik Willis')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['gb_jordan_love']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Jordan Love', stat_qb_name = 'Jordan Love', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Malik Willis', stat_qb_name = 'Malik Willis', home_away = FALSE)
}

rm(team, qb)
#####################################################################