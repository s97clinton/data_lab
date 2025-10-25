##################
#New York Jets
##################

#Get rid of previous Jets seasons
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='NYJ' & run_pass_ref_drive_df$season<2025),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='NYJ' & td_ratio_df$season<2025),]

# pipe in Justin Fields
run_pass_ref_drive_df <- rbind(run_pass_ref_drive_df,fields_df)
td_ratio_df <- rbind(td_ratio_df,fields_td_df)
rm(fields_df,fields_td_df)

