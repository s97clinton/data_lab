###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'SF'
qb <- ifelse(impact_players[['sf_brock_purdy']]==1,'Brock Purdy','Mac Jones')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['sf_brock_purdy']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Brock Purdy', stat_qb_name = 'Brock Purdy', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Mac Jones', stat_qb_name = 'Mac Jones', home_away = FALSE)
}

rm(team, qb)
#####################################################################