###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'CIN'
qb <- ifelse(impact_players[['cin_joe_burrow']]==1,'Joe Burrow','Jake Browning')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['cin_joe_burrow']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Joe Burrow', stat_qb_name = 'Joe Burrow', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Jake Browning', stat_qb_name = 'Jake Browning', home_away = FALSE)
}

rm(team, qb)
#####################################################################