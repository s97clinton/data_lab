#Cincinnati, Joe Burrow 
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='CIN' & run_pass_ref_drive_df$primary_qb!='Joe Burrow'),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='CIN' & td_ratio_df$primary_qb!='Joe Burrow'),]