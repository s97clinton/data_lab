##################
#Kansas City
##################

run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='KC' & run_pass_ref_drive_df$primary_qb!="Patrick Mahomes"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='KC' & td_ratio_df$primary_qb!="Patrick Mahomes"),]

