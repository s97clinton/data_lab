##################
#Tennessee
##################

# Callahan in Tennessee
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='TEN' & run_pass_ref_drive_df$season<2024),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='TEN' & td_ratio_df$season<2024),]



