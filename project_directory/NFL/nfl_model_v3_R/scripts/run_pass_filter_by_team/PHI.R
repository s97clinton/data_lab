##################
#Philly
##################

#Eagles with Jalen Hurts at QB
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='PHI' & run_pass_ref_drive_df$primary_qb!='Jalen Hurts'),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='PHI' & td_ratio_df$primary_qb!='Jalen Hurts'),]

