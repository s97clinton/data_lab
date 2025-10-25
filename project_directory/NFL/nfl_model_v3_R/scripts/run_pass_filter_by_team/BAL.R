#Baltimore
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='BAL' & run_pass_ref_drive_df$designer_offense!='Todd Monken'),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='BAL' & td_ratio_df$designer_offense!='Todd Monken'),]

