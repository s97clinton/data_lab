###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'ARI'
qb <- ifelse(impact_players[['ari_kyler_murray']]==1,'Kyler Murray','Jacoby Brissett')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['ari_kyler_murray']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Kyler Murray', stat_qb_name = 'Kyler Murray', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Jacoby Brissett', stat_qb_name = 'Jacoby Brissett', home_away = TRUE)
}

rm(team, qb)
#####################################################################