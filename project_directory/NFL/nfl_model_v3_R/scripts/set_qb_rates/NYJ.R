###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'NYJ'
qb <- ifelse(impact_players[['nyj_justin_fields']]==1,'Justin Fields','Tyrod Taylor')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['nyj_justin_fields']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Justin Fields', stat_qb_name = 'Justin Fields', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Tyrod Taylor', stat_qb_name = 'Tyrod Taylor', home_away = TRUE)
}

rm(team, qb)
#####################################################################