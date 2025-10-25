##################
#Chicago
##################

#Drop out everything before 2024
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='CHI' & run_pass_ref_drive_df$season<2024),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='CHI' & td_ratio_df$season<2024),]

# pipe in Ben Johnson
run_pass_ref_drive_df <- rbind(run_pass_ref_drive_df,ben_johnson_df)
td_ratio_df <- rbind(td_ratio_df,ben_johnson_td_df)
rm(ben_johnson_df,ben_johnson_td_df)
