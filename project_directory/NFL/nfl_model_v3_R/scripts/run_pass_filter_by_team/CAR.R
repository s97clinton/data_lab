##################
#Carolina
##################

# Carolina 2024 w/ Canales
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='CAR' & run_pass_ref_drive_df$season<2024),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='CAR' & td_ratio_df$season<2024),]
