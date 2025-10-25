#Green Bay
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='GB' & run_pass_ref_drive_df$primary_qb!="Jordan Love"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='GB' & td_ratio_df$primary_qb!="Jordan Love"),]

