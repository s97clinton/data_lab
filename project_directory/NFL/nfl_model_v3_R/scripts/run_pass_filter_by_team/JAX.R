##################
#Jacksonville
##################

run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='JAX' & run_pass_ref_drive_df$primary_qb!="Trevor Lawrence"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='JAX' & td_ratio_df$primary_qb!="Trevor Lawrence"),]