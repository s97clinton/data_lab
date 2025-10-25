###################################
# Set Team, Starting QB, Backup QB
###################################
team <- 'DEN'
qb <- ifelse(impact_players[['den_bo_nix']]==1,'Bo Nix','Jarrett Stidham')
proj_df <- set_team_qb(proj_df = proj_df, team = team, qb = qb)

if (impact_players[['den_bo_nix']]==1) {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Bo Nix', stat_qb_name = 'Bo Nix', home_away = TRUE)
} else {
  proj_df <- set_qb_int_sack_rates(proj_df = proj_df, pfr_pass_df = pfr_pass_df, qb_name = 'Jarrett Stidham', stat_qb_name = 'Jarrett Stidham', home_away = FALSE)
}

rm(team, qb)
#####################################################################