###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'SEA'
qb <- ifelse(impact_players[['sea_sam_darnold']]==1,'Sam Darnold','Drew Lock')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['sea_sam_darnold']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Sam Darnold', stat_qb_name = 'Sam Darnold', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Drew Lock', stat_qb_name = 'Drew Lock', home_away = TRUE)
}

rm(team, qb)
#####################################################################