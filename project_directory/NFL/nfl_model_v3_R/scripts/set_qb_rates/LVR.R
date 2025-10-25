###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'LVR'
qb <- ifelse(impact_players[['lvr_geno_smith']]==1,'Geno Smith',"Kenny Pickett")
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['lvr_geno_smith']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Geno Smith', stat_qb_name = 'Geno Smith', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = "Kenny Pickett", stat_qb_name = "Kenny Pickett", home_away = TRUE)
}

rm(team, qb)
#####################################################################