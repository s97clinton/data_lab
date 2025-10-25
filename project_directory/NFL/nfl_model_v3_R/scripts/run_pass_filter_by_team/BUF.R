##################
#Buffalo
##################
#Set Joe Brady as OC
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='BUF' & run_pass_ref_drive_df$designer_offense!='Joe Brady'),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='BUF' & td_ratio_df$designer_offense!='Joe Brady'),]

