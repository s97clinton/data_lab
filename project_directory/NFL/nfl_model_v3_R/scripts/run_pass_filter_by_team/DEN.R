
#Denver
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='DEN' & run_pass_ref_drive_df$designer_offense!="Sean Payton"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='DEN' & td_ratio_df$designer_offense!="Sean Payton"),]
