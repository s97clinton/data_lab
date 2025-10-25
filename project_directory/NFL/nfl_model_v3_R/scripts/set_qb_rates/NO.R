###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'NO'
qb <- ifelse(impact_players[['no_spencer_rattler']]==1,'Spencer Rattler','Tyler Shough')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['no_spencer_rattler']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Spencer Rattler', stat_qb_name = 'Spencer Rattler', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Tyler Shough', stat_qb_name = 'Mac Jones', home_away = FALSE)
}

rm(team, qb)
#####################################################################