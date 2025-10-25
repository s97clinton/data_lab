#Cleveland, no idea, keep everything, remember when we filtered for Watson...
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='CLE' & run_pass_ref_drive_df$season==2024),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='CLE' & td_ratio_df$season==2024),]


