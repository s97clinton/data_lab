##################
#LA Rams
##################

run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='LAR' & run_pass_ref_drive_df$designer_off!="Sean McVay" & run_pass_ref_drive_df$primary_qb!="Matthew Stafford"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='LAR' & td_ratio_df$designer_off!="Sean McVay"  & td_ratio_df$primary_qb!="Matthew Stafford"),]