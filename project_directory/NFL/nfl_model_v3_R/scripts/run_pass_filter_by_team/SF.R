##################
#San Francisco
##################

run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='SF' & run_pass_ref_drive_df$designer_offense!="Kyle Shannahan" & run_pass_ref_drive_df$backup_qb!="0"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='SF' & td_ratio_df$designer_offense!="Kyle Shannahan" & td_ratio_df$backup_qb!="0"),]
