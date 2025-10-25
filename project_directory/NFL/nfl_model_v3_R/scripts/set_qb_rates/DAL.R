###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'DAL'
qb <- ifelse(impact_players[['dal_dak_prescott']]==1,'Dak Prescott','Joe Milton')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['dal_dak_prescott']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Dak Prescott', stat_qb_name = 'Dak Prescott', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Joe Milton', stat_qb_name = 'Trey Lance', home_away = FALSE)
}

rm(team, qb)
#####################################################################