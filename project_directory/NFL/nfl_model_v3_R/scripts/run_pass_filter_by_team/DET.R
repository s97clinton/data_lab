#Detroit
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='DET' & run_pass_ref_drive_df$primary_qb!="Jared Goff"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='DET' & td_ratio_df$primary_qb!="Jared Goff"),]