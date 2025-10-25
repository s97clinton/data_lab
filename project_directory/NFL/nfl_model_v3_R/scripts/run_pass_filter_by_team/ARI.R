##################
#Arizona
##################
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='ARI' & run_pass_ref_drive_df$designer_offense!='Drew Petzing'),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='ARI' & td_ratio_df$designer_offense!='Drew Petzing'),]

run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='ARI' & run_pass_ref_drive_df$backup_qb== 1),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='ARI' & td_ratio_df$backup_qb== 1),]
