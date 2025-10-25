##################
#Seattle
##################
# Get rid of Hawks pass heavy seasons of past
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='SEA' & run_pass_ref_drive_df$season<2025),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='SEA' & td_ratio_df$season<2025),]

# pipe in Klint Kubiak
run_pass_ref_drive_df <- rbind(run_pass_ref_drive_df,kubiak_df)
td_ratio_df <- rbind(td_ratio_df,kubiak_td_df)
rm(kubiak_df,kubiak_td_df)