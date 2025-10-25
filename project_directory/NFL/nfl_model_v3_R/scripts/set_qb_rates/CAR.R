###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'CAR'
qb <- ifelse(impact_players[['car_bryce_young']]==1,'Bryce Young','Andy Dalton')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['car_bryce_young']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Bryce Young', stat_qb_name = 'Bryce Young', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Andy Dalton', stat_qb_name = 'Andy Dalton', home_away = TRUE)
}

rm(team, qb)
#####################################################################