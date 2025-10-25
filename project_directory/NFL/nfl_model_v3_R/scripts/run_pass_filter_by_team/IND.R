##################
#Indy
##################

# Let's take two years of Steichen
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='IND' & run_pass_ref_drive_df$season<=2022),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='IND' & td_ratio_df$season<=2022),]

