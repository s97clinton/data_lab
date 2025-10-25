###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'CHI'
qb <- ifelse(impact_players[['chi_caleb_williams']]==1,'Caleb Williams','Tyson Bagent')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['chi_caleb_williams']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Caleb Williams', stat_qb_name = 'Caleb Williams', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Tyson Bagent', stat_qb_name = 'Tyson Bagent', home_away = FALSE)
}

rm(team, qb)
#####################################################################