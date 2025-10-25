##################
#New York Giants
##################

run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='NYG' & run_pass_ref_drive_df$designer_offense!="Brian Daboll"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='NYG' & td_ratio_df$designer_offense!="Brian Daboll"),]


