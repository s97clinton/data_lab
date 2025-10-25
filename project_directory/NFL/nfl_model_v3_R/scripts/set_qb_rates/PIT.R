###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'PIT'
qb <- ifelse(impact_players[['pit_aaron_rodgers']]==1,'Aaron Rodgers','Mason Rudolph')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['pit_aaron_rodgers']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Aaron Rodgers', stat_qb_name = 'Aaron Rodgers', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Mason Rudolph', stat_qb_name = 'Mason Rudolph', home_away = TRUE)
}

rm(team, qb)
#####################################################################