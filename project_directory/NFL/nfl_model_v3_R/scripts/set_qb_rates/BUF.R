###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'BUF'
qb <- ifelse(impact_players[['buf_josh_allen']]==1,'Josh Allen','Mitchell Trubisky')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['buf_josh_allen']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Josh Allen', stat_qb_name = 'Josh Allen', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Mitchell Trubisky', stat_qb_name = 'Mitchell Trubisky', home_away = TRUE)
}

rm(team, qb)
#####################################################################