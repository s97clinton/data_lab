#Dallas with  Dak Prescott at QB
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='DAL' & run_pass_ref_drive_df$primary_qb!='Dak Prescott'),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='DAL' & td_ratio_df$primary_qb!='Dak Prescott'),]