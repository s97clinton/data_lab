#Houston
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='HOU' & run_pass_ref_drive_df$primary_qb!="C.J. Stroud"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='HOU' & td_ratio_df$primary_qb!="C.J. Stroud"),]
