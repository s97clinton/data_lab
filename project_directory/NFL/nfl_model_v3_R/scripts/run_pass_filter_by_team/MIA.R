##################
#Miami
##################

# Roll with Mike McDaniel
run_pass_ref_drive_df <- run_pass_ref_drive_df[!(run_pass_ref_drive_df$off=='MIA' & run_pass_ref_drive_df$designer_off!='Mike McDaniel'),]
td_ratio_df <- td_ratio_df[!(td_ratio_df$team=='MIA' & td_ratio_df$designer_off!='Mike McDaniel'),]