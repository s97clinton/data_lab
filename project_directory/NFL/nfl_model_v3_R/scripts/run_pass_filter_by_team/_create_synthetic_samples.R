##########################
## Synthetic team Samples
##########################

##########################
## Chicago (Ben Johnson)
##########################
#Ben Johnson in Detroit
ben_johnson_df <- run_pass_ref_drive_df[(run_pass_ref_drive_df$off=='DET' & run_pass_ref_drive_df$designer_offense=='Ben Johnson'),]
ben_johnson_df$off <- ifelse(ben_johnson_df$off=='DET','CHI',as.character(ben_johnson_df$off))
ben_johnson_df$season <- ifelse(ben_johnson_df$season==2024,2014,ben_johnson_df$season)
ben_johnson_df$season <- ifelse(ben_johnson_df$season==2023,2013,ben_johnson_df$season)
ben_johnson_df$season <- ifelse(ben_johnson_df$season==2022,2012,ben_johnson_df$season)

ben_johnson_td_df <- td_ratio_df[(td_ratio_df$team=='DET' & td_ratio_df$designer_offense=='Ben Johnson'),]
ben_johnson_td_df$team <- ifelse(ben_johnson_td_df$team=='DET','CHI',as.character(ben_johnson_td_df$team))
ben_johnson_td_df$season <- ifelse(ben_johnson_td_df$season==2024,2014,as.character(ben_johnson_td_df$season))
ben_johnson_td_df$season <- ifelse(ben_johnson_td_df$season==2023,2013,as.character(ben_johnson_td_df$season))
ben_johnson_td_df$season <- ifelse(ben_johnson_td_df$season==2022,2012,as.character(ben_johnson_td_df$season))

##############################
## Minnesota (pound the rock)
##############################
#Kevin O'Connell pull in some of what Rams have brought to table last two years
vikings_run_ball_df <- run_pass_ref_drive_df[(run_pass_ref_drive_df$off=='BAL' & run_pass_ref_drive_df$season==2022),]
vikings_run_ball_df$off <- ifelse(vikings_run_ball_df$off=='BAL','MIN',as.character(vikings_run_ball_df$off))
vikings_run_ball_df$season <- ifelse(vikings_run_ball_df$season==2024,2014,vikings_run_ball_df$season)
vikings_run_ball_df$season <- ifelse(vikings_run_ball_df$season==2023,2013,vikings_run_ball_df$season)

vikings_run_ball_td <- td_ratio_df[(td_ratio_df$team=='PHI' & td_ratio_df$season!=2022),]
vikings_run_ball_td$team <- ifelse(vikings_run_ball_td$team=='PHI','MIN',as.character(vikings_run_ball_td$team))
vikings_run_ball_td$season <- ifelse(vikings_run_ball_td$season==2024,2014,as.character(vikings_run_ball_td$season))
vikings_run_ball_td$season <- ifelse(vikings_run_ball_td$season==2023,2013,as.character(vikings_run_ball_td$season))


##################################
## New York Jets (Justin Fields)
##################################
# pipe in Justin Fields's tour of duty
fields_df <- run_pass_ref_drive_df[(run_pass_ref_drive_df$primary_qb=='Justin Fields'  & run_pass_ref_drive_df$season<2025),]
fields_df$off <- ifelse(fields_df$off!='NYJ','NYJ',as.character(fields_df$off))
fields_df$season <- ifelse(fields_df$season==2024,2014,fields_df$season)
fields_df$season <- ifelse(fields_df$season==2023,2013,fields_df$season)
fields_df$season <- ifelse(fields_df$season==2022,2012,fields_df$season)
fields_df$season <- ifelse(fields_df$season==2021,2011,fields_df$season)

fields_td_df <- td_ratio_df[(td_ratio_df$primary_qb=='Justin Fields' & td_ratio_df$season<2025),]
fields_td_df$team <- ifelse(fields_td_df$team!='NYJ','NYJ',as.character(fields_td_df$team))
fields_td_df$season <- ifelse(fields_td_df$season==2024,2014,as.character(fields_td_df$season))
fields_td_df$season <- ifelse(fields_td_df$season==2023,2013,as.character(fields_td_df$season))
fields_td_df$season <- ifelse(fields_td_df$season==2022,2012,as.character(fields_td_df$season))
fields_td_df$season <- ifelse(fields_td_df$season==2021,2011,as.character(fields_td_df$season))


##################################
## Seattle (Klint Kubiak)
##################################
# pipe in Klint Kubiak's tour of duty
kubiak_df <- run_pass_ref_drive_df[(run_pass_ref_drive_df$playcaller_off=='Klint Kubiak'  & run_pass_ref_drive_df$season<2025),]
kubiak_df$off <- ifelse(kubiak_df$off!='SEA','SEA',as.character(kubiak_df$off))
kubiak_df$season <- ifelse(kubiak_df$season==2024,2014,kubiak_df$season)
kubiak_df$season <- ifelse(kubiak_df$season==2022,2012,kubiak_df$season)
kubiak_df$season <- ifelse(kubiak_df$season==2021,2011,kubiak_df$season)

kubiak_td_df <- td_ratio_df[(td_ratio_df$playcaller_off=='Klint Kubiak' & td_ratio_df$season<2025),]
kubiak_td_df$team <- ifelse(kubiak_td_df$team!='SEA','SEA',as.character(kubiak_td_df$team))
kubiak_td_df$season <- ifelse(kubiak_td_df$season==2024,2014,as.character(kubiak_td_df$season))
kubiak_td_df$season <- ifelse(kubiak_td_df$season==2022,2012,as.character(kubiak_td_df$season))
kubiak_td_df$season <- ifelse(kubiak_td_df$season==2021,2011,as.character(kubiak_td_df$season))








