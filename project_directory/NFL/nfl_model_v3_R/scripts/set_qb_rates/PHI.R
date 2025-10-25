###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'PHI'
qb <- ifelse(impact_players[['phi_jalen_hurts']]==1,'Jalen Hurts','Sam Howell')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['phi_jalen_hurts']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Jalen Hurts', stat_qb_name = 'Jalen Hurts', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Sam Howell', stat_qb_name = 'Sam Howell', home_away = TRUE)
}

rm(team, qb)
#####################################################################