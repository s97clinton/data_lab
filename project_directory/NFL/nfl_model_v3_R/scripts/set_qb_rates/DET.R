###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'DET'
qb <- ifelse(impact_players[['det_jared_goff']]==1,'Jared Goff','Kyle Allen')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['det_jared_goff']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Jared Goff', stat_qb_name = 'Jared Goff', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Kyle Allen', stat_qb_name = 'Kyle Allen', home_away = FALSE)
}

rm(team, qb)
#####################################################################