##################
# Pittsburgh 
##################
# Arthur Smith in Pittsburgh
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='PIT' & run_pass_ref_drive_df$season<2024),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='PIT' & td_ratio_df$season<2022),]

