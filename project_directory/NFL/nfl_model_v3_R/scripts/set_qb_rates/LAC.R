###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'LAC'
qb <- ifelse(impact_players[['lac_justin_herbert']]==1,'Justin Herbert','Trey Lance')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['lac_justin_herbert']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Justin Herbert', stat_qb_name = 'Justin Herbert', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Trey Lance', stat_qb_name = 'Trey Lance', home_away = FALSE)
}

rm(team, qb)
#####################################################################