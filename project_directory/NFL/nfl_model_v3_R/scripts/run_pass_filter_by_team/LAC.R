##################
#LA Chargers
##################

# Cut to Justin Herbert games, but need to add in a Harbaugh/Roman influence
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='LAC' & run_pass_ref_drive_df$season<2024),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='LAC' & td_ratio_df$season<2024),]