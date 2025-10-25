###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'IND'
qb <- ifelse(impact_players[['ind_daniel_jones']]==1,'Daniel Jones','Anthony Richardson')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['ind_daniel_jones']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Daniel Jones', stat_qb_name = 'Daniel Jones', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Anthony Richardson', stat_qb_name = 'Anthony Richardson', home_away = TRUE)
}

rm(team, qb)
#####################################################################