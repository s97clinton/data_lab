##################
#Minnesota
##################

run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='MIN' & run_pass_ref_drive_df$designer_off=="Kevin O'Connell"),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='MIN' & td_ratio_df$designer_off=="Kevin O'Connell"),]

# pipe in run influence
run_pass_ref_drive_df <- rbind(run_pass_ref_drive_df,vikings_run_ball_df)
td_ratio_df <- rbind(td_ratio_df,vikings_run_ball_td)
rm(vikings_run_ball_df,vikings_run_ball_td)

