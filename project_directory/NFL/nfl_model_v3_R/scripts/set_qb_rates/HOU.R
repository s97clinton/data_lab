###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'HOU'
qb <- ifelse(impact_players[['hou_cj_stroud']]==1,'C.J. Stroud','Davis Mills')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['hou_cj_stroud']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'C.J. Stroud', stat_qb_name = 'C.J. Stroud', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Davis Mills', stat_qb_name = 'Davis Mills', home_away = TRUE)
}

rm(team, qb)
#####################################################################