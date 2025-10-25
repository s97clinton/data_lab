##################
#Atlanta     
##################
# Zac Robinson Year One
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='ATL' & run_pass_ref_drive_df$season<2024),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='ATL' & td_ratio_df$season<2024),]


