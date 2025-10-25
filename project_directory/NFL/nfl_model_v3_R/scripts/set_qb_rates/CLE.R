###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'CLE'
qb <- ifelse(impact_players[['cle_joe_flacco']]==1,'Joe Flacco','Dillon Gabriel')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['cle_joe_flacco']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Joe Flacco', stat_qb_name = 'Joe Flacco', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Dillon Gabriel', stat_qb_name = 'Kenny Pickett', home_away = TRUE)
}

rm(team, qb)
#####################################################################