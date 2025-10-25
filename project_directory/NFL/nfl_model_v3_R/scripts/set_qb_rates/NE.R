###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'NE'
qb <- ifelse(impact_players[['ne_drake_maye']]==1,'Drake Maye','Joshua Dobbs')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['ne_drake_maye']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Drake Maye', stat_qb_name = 'Drake Maye', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Joshua Dobbs', stat_qb_name = 'Joshua Dobbs', home_away = TRUE)
}

rm(team, qb)
#####################################################################