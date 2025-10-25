##################
# Tampa Bay
##################

# Cut everything before Baker Mayfield
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='TB' & run_pass_ref_drive_df$primary_qb!="Baker Mayfield"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='TB' & td_ratio_df$primary_qb!="Baker Mayfield"),]


