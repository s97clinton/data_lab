###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'JAX'
qb <- ifelse(impact_players[['jax_trevor_lawrence']]==1,'Trevor Lawrence','Nick Mullens')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['jax_trevor_lawrence']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Trevor Lawrence', stat_qb_name = 'Trevor Lawrence', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Nick Mullens', stat_qb_name = 'Nick Mullens', home_away = FALSE)
}

rm(team, qb)
#####################################################################