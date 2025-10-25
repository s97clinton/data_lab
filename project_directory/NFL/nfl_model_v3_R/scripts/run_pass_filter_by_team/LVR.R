##################
#Las Vegas
##################

# Vegas has more moderate run/pass break in 2022, 2023, expect Chip Kelly to run a balanced offense with Ashton Jeanty in fold.
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='LVR' & run_pass_ref_drive_df$season==2024),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='LVR' & td_ratio_df$season==2024),]

# Add in a run-heavy df, copy Vikings
run_pass_ref_drive_df <- rbind(run_pass_ref_drive_df,vikings_run_ball_df)