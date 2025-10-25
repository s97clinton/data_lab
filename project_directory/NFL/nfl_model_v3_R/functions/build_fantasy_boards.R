library(dplyr)
library(tidyr)
library(purrr)

prep_consensus_qb_to_merge <- function(no_ppr_path, half_ppr_path, full_ppr_path, output_path){
  no_ppr_ranks <- read.csv(no_ppr_path)
  half_ppr_ranks <- read.csv(half_ppr_path)
  full_ppr_ranks <- read.csv(full_ppr_path)
  
  no_ppr_qb_ranks <- no_ppr_ranks[grepl("QB",no_ppr_ranks$pos_rank), ]
  half_ppr_qb_ranks <- half_ppr_ranks[grepl("QB",half_ppr_ranks$pos_rank), ]
  full_ppr_qb_ranks <- full_ppr_ranks[grepl("QB",full_ppr_ranks$pos_rank), ]
  
  no_ppr_qb_merge <- subset(no_ppr_qb_ranks, select=c("team","player","bye","pos_rank","tier","ovr_rank"))
  names(no_ppr_qb_merge) <- c("team","player_name","bye","consensus_pos_rank","consensus_tier_no_ppr","consensus_ovr_rank_no_ppr")
  half_ppr_qb_merge <- subset(half_ppr_qb_ranks, select=c("team","player","bye","tier","ovr_rank"))
  names(half_ppr_qb_merge) <- c("team","player_name","bye","consensus_tier_half_ppr","consensus_ovr_rank_half_ppr")
  full_ppr_qb_merge <- subset(full_ppr_qb_ranks, select=c("team","player","bye","tier","ovr_rank"))
  names(full_ppr_qb_merge) <- c("team","player_name","bye","consensus_tier_full_ppr","consensus_ovr_rank_full_ppr")
  
  qb_consensus_df <- merge(no_ppr_qb_merge, half_ppr_qb_merge, by = c("team","player_name","bye"))
  qb_consensus_df <- merge(qb_consensus_df, full_ppr_qb_merge, by = c("team","player_name","bye"))
  
  qb_consensus_df <- qb_consensus_df %>%
    mutate(team = recode(team,
                         "JAC" = "JAX",
                         "LV" = "LVR",
                         "WAS" = "WSH"))
  
  qb_consensus_df <- qb_consensus_df %>%
    mutate(player_name = recode(player_name,
                                "Patrick Mahomes II" = "Patrick Mahomes",
                                "Michael Penix Jr." = "Michael Penix",
                                "Cameron Ward" = "Cam Ward"))
  
  write.csv(qb_consensus_df, paste0(output_path))
}

prep_consensus_skill_to_merge <- function(no_ppr_path, half_ppr_path, full_ppr_path, output_path){
  no_ppr_ranks <- read.csv(no_ppr_path)
  half_ppr_ranks <- read.csv(half_ppr_path)
  full_ppr_ranks <- read.csv(full_ppr_path)
  
  no_ppr_skill_ranks <- no_ppr_ranks[!grepl("QB",no_ppr_ranks$pos_rank), ]
  no_ppr_skill_ranks <- no_ppr_skill_ranks[!grepl("K",no_ppr_skill_ranks$pos_rank), ]
  no_ppr_skill_ranks <- no_ppr_skill_ranks[!grepl("DST",no_ppr_skill_ranks$pos_rank), ]
  half_ppr_skill_ranks <- half_ppr_ranks[!grepl("QB",half_ppr_ranks$pos_rank), ]
  half_ppr_skill_ranks <- half_ppr_skill_ranks[!grepl("K",half_ppr_skill_ranks$pos_rank), ]
  half_ppr_skill_ranks <- half_ppr_skill_ranks[!grepl("DST",half_ppr_skill_ranks$pos_rank), ]
  full_ppr_skill_ranks <- full_ppr_ranks[!grepl("QB",full_ppr_ranks$pos_rank), ]
  full_ppr_skill_ranks <- full_ppr_skill_ranks[!grepl("K",full_ppr_skill_ranks$pos_rank), ]
  full_ppr_skill_ranks <- full_ppr_skill_ranks[!grepl("DST",full_ppr_skill_ranks$pos_rank), ]
  
  no_ppr_skill_merge <- subset(no_ppr_skill_ranks, select=c("team","player","bye","pos_rank","tier","ovr_rank"))
  names(no_ppr_skill_merge) <- c("team","player_name","bye","consensus_pos_rank_no_ppr","consensus_tier_no_ppr","consensus_ovr_rank_no_ppr")
  half_ppr_skill_merge <- subset(half_ppr_skill_ranks, select=c("team","player","bye","pos_rank","tier","ovr_rank"))
  names(half_ppr_skill_merge) <- c("team","player_name","bye","consensus_pos_rank_half_ppr","consensus_tier_half_ppr","consensus_ovr_rank_half_ppr")
  full_ppr_skill_merge <- subset(full_ppr_skill_ranks, select=c("team","player","bye","pos_rank","tier","ovr_rank"))
  names(full_ppr_skill_merge) <- c("team","player_name","bye","consensus_pos_rank_full_ppr","consensus_tier_full_ppr","consensus_ovr_rank_full_ppr")
  
  skill_consensus_df <- merge(no_ppr_skill_merge, half_ppr_skill_merge, by = c("team","player_name","bye"))
  skill_consensus_df <- merge(skill_consensus_df, full_ppr_skill_merge, by = c("team","player_name","bye"))
  
  skill_consensus_df <- skill_consensus_df %>%
    mutate(team = recode(team,
                         "JAC" = "JAX",
                         "LV" = "LVR",
                         "WAS" = "WSH"))

  skill_consensus_df <- skill_consensus_df %>%
    mutate(player_name = recode(player_name,
                                "DeMario Douglas" = "Demario Douglas",
                                "Travis Etienne Jr." = "Travis Etienne",
                                "RJ Harvey" = "R.J. Harvey",
                                "Tre' Harris" = "Tre Harris",
                                "Aaron Jones Sr." = "Aaron Jones",
                                "Ray-Ray McCloud III" = "Ray-Ray McCloud",
                                "DK Metcalf" = "D.K. Metcalf",
                                "Marvin Mims Jr." = "Marvin Mims",
                                "DJ Moore" = "D.J. Moore",
                                "Chig Okonkwo" = "Chigoziem Okonkwo",
                                "Joshua Palmer" = "Josh Palmer",
                                "Kyle Pitts Sr." = "Kyle Pitts",
                                "Deebo Samuel Sr." = "Deebo Samuel",
                                "Brian Thomas Jr." = "Brian Thomas"))
    
  write.csv(skill_consensus_df, paste0(output_path))
}

build_qb_board <- function(pass_stats_df, rush_stats_df) {
  qb_board <- merge(pass_stats_df, rush_stats_df, by = c("key","team","pos","player_name"), all.x = TRUE)
  qb_board$fantasy <- round((qb_board$pass_yds*0.04)+(qb_board$pass_td*4)+(qb_board$rush_yds*0.1)+(qb_board$rush_td*6)-(qb_board$interceptions*2) , 2)
  qb_board$te_premium <- round((qb_board$pass_yds*0.05)+(qb_board$pass_td*4)+(qb_board$rush_yds*0.1)+(qb_board$rush_td*6)-(qb_board$interceptions*2) , 2)
  return(qb_board)
}

build_skill_board <- function(rush_stats_df, rec_stats_df) {
  skill_board <- merge(rush_stats_df, rec_stats_df, by = c("key","team","pos","player_name"), all = TRUE)
  skill_board <- skill_board[(skill_board$pos != "QB"),]
  skill_board <- replace(skill_board, is.na(skill_board), 0)
  skill_board$no_ppr <- round((skill_board$rush_yds*0.1)+(skill_board$rush_td*6)+(skill_board$receptions*0)+(skill_board$rec_yds*0.1)+(skill_board$rec_td*6), 2)
  skill_board$half_ppr <- round((skill_board$rush_yds*0.1)+(skill_board$rush_td*6)+(skill_board$receptions*0.5)+(skill_board$rec_yds*0.1)+(skill_board$rec_td*6), 2)
  skill_board$full_ppr <- round((skill_board$rush_yds*0.1)+(skill_board$rush_td*6)+(skill_board$receptions*1)+(skill_board$rec_yds*0.1)+(skill_board$rec_td*6), 2)
  skill_board$te_premium <- ifelse(skill_board$pos == 'TE', skill_board$full_ppr + skill_board$receptions*0.5, skill_board$full_ppr)
  return(skill_board)
}

add_no_ppr_qb_fantasy_tier <- function(df) {
  df <- df %>%
    mutate(no_ppr_fantasy_tier = case_when(
      fantasy_per_gm >= 22 ~ 3,
      fantasy_per_gm >= 21 ~ 4,
      fantasy_per_gm >= 20 ~ 5,
      fantasy_per_gm >= 19 ~ 6,
      fantasy_per_gm >= 17 ~ 9,
      fantasy_per_gm >= 16 ~ 10,
      fantasy_per_gm >= 15 ~ 11,
      fantasy_per_gm >= 14 ~ 12,
      fantasy_per_gm >= 13 ~ 13,
      fantasy_per_gm >= 12 ~ 14,
      TRUE ~ 22
    ))
  return(df)
}

add_half_ppr_qb_fantasy_tier <- function(df) {
  df <- df %>%
    mutate(half_ppr_fantasy_tier = case_when(
      fantasy_per_gm >= 22 ~ 3,
      fantasy_per_gm >= 21 ~ 4,
      fantasy_per_gm >= 20 ~ 5,
      fantasy_per_gm >= 19 ~ 6,
      fantasy_per_gm >= 17 ~ 9,
      fantasy_per_gm >= 16 ~ 10,
      fantasy_per_gm >= 15 ~ 11,
      fantasy_per_gm >= 14 ~ 12,
      fantasy_per_gm >= 13 ~ 13,
      fantasy_per_gm >= 12 ~ 14,
      TRUE ~ 22
    ))
  return(df)
}

add_full_ppr_qb_fantasy_tier <- function(df) {
  df <- df %>%
    mutate(full_ppr_fantasy_tier = case_when(
      fantasy_per_gm >= 20 ~ 6,
      fantasy_per_gm >= 19 ~ 7,
      fantasy_per_gm >= 17 ~ 9,
      fantasy_per_gm >= 16 ~ 10,
      fantasy_per_gm >= 15 ~ 11,
      fantasy_per_gm >= 14 ~ 12,
      fantasy_per_gm >= 13 ~ 13,
      fantasy_per_gm >= 12 ~ 14,
      TRUE ~ 22
    ))
  return(df)
}

add_te_premium_qb_fantasy_tier <- function(df) {
  df <- df %>%
    mutate(te_premium_fantasy_tier = case_when(
      te_premium_per_gm >= 22 ~ 3,
      te_premium_per_gm >= 21 ~ 4,
      te_premium_per_gm >= 20 ~ 5,
      te_premium_per_gm >= 19 ~ 6,
      te_premium_per_gm >= 17 ~ 9,
      te_premium_per_gm >= 16 ~ 10,
      te_premium_per_gm >= 15 ~ 11,
      te_premium_per_gm >= 14 ~ 12,
      te_premium_per_gm >= 13 ~ 13,
      te_premium_per_gm >= 12 ~ 14,
      TRUE ~ 22
    ))
  return(df)
}

add_no_ppr_fantasy_tier <- function(df) {
  df <- df %>%
    mutate(no_ppr_fantasy_tier = case_when(
      no_ppr_per_gm >= 16 ~ 0,
      no_ppr_per_gm >= 15 ~ 1,
      no_ppr_per_gm >= 14 ~ 2,
      no_ppr_per_gm >= 13 ~ 3,
      no_ppr_per_gm >= 12 ~ 4,
      no_ppr_per_gm >= 11 ~ 5,
      no_ppr_per_gm >= 10 ~ 6,
      no_ppr_per_gm >= 9 ~ 7,
      no_ppr_per_gm >= 8 ~ 8,
      no_ppr_per_gm >= 7 ~ 9,
      no_ppr_per_gm >= 6 ~ 10,
      no_ppr_per_gm >= 5 ~ 11,
      no_ppr_per_gm >= 4 ~ 12,
      no_ppr_per_gm >= 3 ~ 13,
      TRUE ~ 22
    ))
  return(df)
}

add_half_ppr_fantasy_tier <- function(df) {
  df <- df %>%
    mutate(half_ppr_fantasy_tier = case_when(
      half_ppr_per_gm >= 17 ~ 0,
      half_ppr_per_gm >= 16 ~ 1,
      half_ppr_per_gm >= 15 ~ 2,
      half_ppr_per_gm >= 14 ~ 3,
      half_ppr_per_gm >= 13 ~ 4,
      half_ppr_per_gm >= 12 ~ 5,
      half_ppr_per_gm >= 11 ~ 6,
      half_ppr_per_gm >= 10 ~ 7,
      half_ppr_per_gm >= 9 ~ 8,
      half_ppr_per_gm >= 8 ~ 9,
      half_ppr_per_gm >= 7 ~ 10,
      half_ppr_per_gm >= 6 ~ 11,
      half_ppr_per_gm >= 5 ~ 12,
      half_ppr_per_gm >= 4 ~ 13,
      TRUE ~ 22
    ))
  return(df)
}

add_full_ppr_fantasy_tier <- function(df) {
  df <- df %>%
    mutate(full_ppr_fantasy_tier = case_when(
      full_ppr_per_gm >= 19 ~ 0,
      full_ppr_per_gm >= 18 ~ 1,
      full_ppr_per_gm >= 17 ~ 2,
      full_ppr_per_gm >= 16 ~ 3,
      full_ppr_per_gm >= 15 ~ 4,
      full_ppr_per_gm >= 14 ~ 5,
      full_ppr_per_gm >= 13 ~ 6,
      full_ppr_per_gm >= 12 ~ 7,
      full_ppr_per_gm >= 11 ~ 8,
      full_ppr_per_gm >= 10 ~ 9,
      full_ppr_per_gm >= 9 ~ 10,
      TRUE ~ 11
    ))
  return(df)
}

add_te_premium_fantasy_tier <- function(df) {
  df <- df %>%
    mutate(te_premium_fantasy_tier = case_when(
      te_premium_per_gm >= 19 ~ 0,
      te_premium_per_gm >= 18 ~ 1,
      te_premium_per_gm >= 17 ~ 2,
      te_premium_per_gm >= 16 ~ 3,
      te_premium_per_gm >= 15 ~ 4,
      te_premium_per_gm >= 14 ~ 5,
      te_premium_per_gm >= 13 ~ 6,
      te_premium_per_gm >= 12 ~ 7,
      te_premium_per_gm >= 11 ~ 8,
      te_premium_per_gm >= 10 ~ 9,
      te_premium_per_gm >= 9 ~ 10,
      te_premium_per_gm >= 8 ~ 11,
      te_premium_per_gm >= 7 ~ 12,
      te_premium_per_gm >= 6 ~ 13,
      TRUE ~ 22
    ))
  return(df)
}

aggregate_qb_season_stats <- function(path, consensus_path, output_path){
  files <- list.files(path = path, pattern = "*.csv", full.names = TRUE)
  qb_data <- files %>%
    lapply(read.csv) %>%
    bind_rows()
  
  agg_qb_stats <- aggregate(
    x = qb_data[, c("pass_attempts", "completions", "pass_yds", "pass_td", "interceptions", "carries", "rush_yds", "rush_td", "fantasy", "te_premium")],
    by = list(team = qb_data$team, pos = qb_data$pos, player_name = qb_data$player_name),
    FUN = sum,
    na.rm = TRUE
  )
  agg_qb_stats$fantasy_per_gm <- round(agg_qb_stats$fantasy/17, 2)
  agg_qb_stats$te_premium_per_gm <- round(agg_qb_stats$te_premium/17, 2)
  
  agg_qb_stats <- agg_qb_stats %>%
    arrange(desc(fantasy)) %>%
    mutate(pos_rank = paste0("QB", row_number()))
  
  agg_qb_stats <- add_no_ppr_qb_fantasy_tier(agg_qb_stats)
  agg_qb_stats <- add_half_ppr_qb_fantasy_tier(agg_qb_stats)
  agg_qb_stats <- add_full_ppr_qb_fantasy_tier(agg_qb_stats)
  agg_qb_stats <- add_te_premium_qb_fantasy_tier(agg_qb_stats)
  
  consensus_qb_ranks <- read.csv(consensus_path)
  agg_qb_stats <- merge(agg_qb_stats, consensus_qb_ranks, by=c("team","player_name"), all.x = TRUE)
  
  write.csv(agg_qb_stats, paste0(output_path))
  return(agg_qb_stats)
}

aggregate_skill_season_stats <- function(path, consensus_path, output_path){
  files <- list.files(path = path, pattern = "*.csv", full.names = TRUE)
  skill_data <- files %>%
    lapply(read.csv) %>%
    bind_rows()
  
  agg_skill_stats <- aggregate(
    x = skill_data[, c("carries", "rush_yds", "rush_td", "targets", "receptions", "rec_yds", "rec_td", "no_ppr", "half_ppr", "full_ppr", "te_premium")],
    by = list(team = skill_data$team, pos = skill_data$pos, player_name = skill_data$player_name),
    FUN = sum,
    na.rm = TRUE
  )
  agg_skill_stats$no_ppr_per_gm <- round(agg_skill_stats$no_ppr/17, 2)
  agg_skill_stats$half_ppr_per_gm <- round(agg_skill_stats$half_ppr/17, 2)
  agg_skill_stats$full_ppr_per_gm <- round(agg_skill_stats$full_ppr/17, 2)
  agg_skill_stats$te_premium_per_gm <- round(agg_skill_stats$te_premium/17, 2)
  
  agg_skill_stats <- agg_skill_stats %>%
    arrange(desc(no_ppr)) %>%
    mutate(no_ppr_skill_rank = row_number()) %>%
    group_by(pos) %>%
    mutate(no_ppr_pos_rank = paste0(pos, row_number())) %>%
    ungroup()
  
  agg_skill_stats <- agg_skill_stats %>%
    arrange(desc(half_ppr)) %>%
    mutate(half_ppr_skill_rank = row_number()) %>%
    group_by(pos) %>%
    mutate(half_ppr_pos_rank = paste0(pos, row_number())) %>%
    ungroup()
  
  agg_skill_stats <- agg_skill_stats %>%
    arrange(desc(full_ppr)) %>%
    mutate(full_ppr_skill_rank = row_number()) %>%
    group_by(pos) %>%
    mutate(full_ppr_pos_rank = paste0(pos, row_number())) %>%
    ungroup()
  
  agg_skill_stats <- add_no_ppr_fantasy_tier(agg_skill_stats)
  agg_skill_stats <- add_half_ppr_fantasy_tier(agg_skill_stats)
  agg_skill_stats <- add_full_ppr_fantasy_tier(agg_skill_stats)
  agg_skill_stats <- add_te_premium_fantasy_tier(agg_skill_stats)
  
  consensus_skill_ranks <- read.csv(consensus_path)
  agg_skill_stats <- merge(agg_skill_stats, consensus_skill_ranks, by=c("team","player_name"), all.x = TRUE)
  agg_skill_stats$half_ppr_ovr_rank_diff <- agg_skill_stats$consensus_ovr_rank_half_ppr - agg_skill_stats$half_ppr_skill_rank
  
  write.csv(agg_skill_stats, paste0(output_path))
  return(agg_skill_stats)
}

build_no_ppr_board <- function(agg_qb_stats, agg_skill_stats, output_path){
  combined_board_qb <- subset(agg_qb_stats, select = c("team","pos","player_name","fantasy_per_gm","no_ppr_fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank_no_ppr"))
  colnames(combined_board_qb) <- c("team","pos","player_name","no_ppr_per_gm","fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank")
  combined_board_skill <- subset(agg_skill_stats, select = c("team","pos","player_name","no_ppr_per_gm","no_ppr_fantasy_tier","no_ppr_pos_rank","consensus_pos_rank_no_ppr","consensus_ovr_rank_no_ppr"))
  colnames(combined_board_skill) <- c("team","pos","player_name","no_ppr_per_gm","fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank")
  combined_board <- rbind(combined_board_qb, combined_board_skill)
  
  combined_board$fantasy_tier <- ifelse(combined_board$pos == "TE", combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "De'Von Achane" & combined_board$fantasy_tier<=1, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Ladd McConkey" & combined_board$fantasy_tier<=2, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Christian McCaffrey" & combined_board$fantasy_tier>=3, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Ashton Jeanty" & combined_board$fantasy_tier>=3, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Lamar Jackson" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Josh Allen" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jalen Hurts" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Mike Evans" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Breece Hall" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Davante Adams" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tee Higgins" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Joe Burrow" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Trey McBride" & combined_board$fantasy_tier>=5, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jakobi Meyers" & combined_board$fantasy_tier<=5, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "TreVeyon Henderson" & combined_board$fantasy_tier>=6, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Brock Purdy" & combined_board$fantasy_tier<=7, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Calvin Ridley" & combined_board$fantasy_tier>=8, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "David Njoku" & combined_board$fantasy_tier<=8, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  
  pos_order <- c("TE" = 1, "WR" = 2, "RB" = 3, "QB" = 4)
  combined_board$sort_rank <- as.numeric(sub("^[A-Z]+", "", combined_board$pos_rank))
  combined_board <- combined_board[order(combined_board$fantasy_tier, pos_order[combined_board$pos], combined_board$sort_rank), ]
  combined_board <- combined_board[, !names(combined_board) %in% c("sort_rank")]
  
  rownames(combined_board) <- NULL
  combined_board$ovr_rank <- seq_len(nrow(combined_board))
  combined_board <- subset(combined_board, select = c("team","pos","player_name","no_ppr_per_gm","fantasy_tier","pos_rank","consensus_pos_rank", "ovr_rank","consensus_ovr_rank"))
  combined_board$diff_from_consensus <- combined_board$consensus_ovr_rank - combined_board$ovr_rank
  
  combined_board <- combined_board %>%
    mutate(pos_rank = row_number()) %>%
    group_by(pos) %>%
    mutate(pos_rank = paste0(pos, row_number())) %>%
    ungroup()
  
  write.csv(combined_board, paste0(output_path))
}

build_half_ppr_board <- function(agg_qb_stats, agg_skill_stats, output_path){
  combined_board_qb <- subset(agg_qb_stats, select = c("team","pos","player_name","fantasy_per_gm","half_ppr_fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank_half_ppr"))
  colnames(combined_board_qb) <- c("team","pos","player_name","half_ppr_per_gm","fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank")
  combined_board_skill <- subset(agg_skill_stats, select = c("team","pos","player_name","half_ppr_per_gm","half_ppr_fantasy_tier","half_ppr_pos_rank","consensus_pos_rank_half_ppr","consensus_ovr_rank_half_ppr"))
  colnames(combined_board_skill) <- c("team","pos","player_name","half_ppr_per_gm","fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank")
  combined_board <- rbind(combined_board_qb, combined_board_skill)
  
  combined_board$fantasy_tier <- ifelse(combined_board$pos == "RB" & combined_board$fantasy_tier>=6, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$pos == "TE", combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "De'Von Achane" & combined_board$fantasy_tier<=1, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Ladd McConkey" & combined_board$fantasy_tier<=2, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Christian McCaffrey" & combined_board$fantasy_tier>=3, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Ashton Jeanty" & combined_board$fantasy_tier>=3, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Lamar Jackson" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Josh Allen" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jalen Hurts" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Mike Evans" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Breece Hall" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Davante Adams" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tee Higgins" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Joe Burrow" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Trey McBride" & combined_board$fantasy_tier>=5, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jakobi Meyers" & combined_board$fantasy_tier<=5, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Travis Hunter" & combined_board$fantasy_tier<=5, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "TreVeyon Henderson" & combined_board$fantasy_tier>=6, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Brock Purdy" & combined_board$fantasy_tier<=7, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Calvin Ridley" & combined_board$fantasy_tier>=8, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "David Njoku" & combined_board$fantasy_tier<=8, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  
  pos_order <- c("TE" = 1, "WR" = 2, "RB" = 3, "QB" = 4)
  combined_board$sort_rank <- as.numeric(sub("^[A-Z]+", "", combined_board$pos_rank))
  combined_board <- combined_board[order(combined_board$fantasy_tier, pos_order[combined_board$pos], combined_board$sort_rank), ]
  combined_board <- combined_board[, !names(combined_board) %in% c("sort_rank")]
  
  rownames(combined_board) <- NULL
  combined_board$ovr_rank <- seq_len(nrow(combined_board))
  combined_board <- subset(combined_board, select = c("team","pos","player_name","half_ppr_per_gm","fantasy_tier","pos_rank","consensus_pos_rank", "ovr_rank","consensus_ovr_rank"))
  combined_board$diff_from_consensus <- combined_board$consensus_ovr_rank - combined_board$ovr_rank
  
  combined_board <- combined_board %>%
    mutate(pos_rank = row_number()) %>%
    group_by(pos) %>%
    mutate(pos_rank = paste0(pos, row_number())) %>%
    ungroup()
  
  write.csv(combined_board, paste0(output_path))
}

build_full_ppr_board <- function(agg_qb_stats, agg_skill_stats, output_path, output_path_2){
  combined_board_qb <- subset(agg_qb_stats, select = c("team","pos","player_name","fantasy_per_gm","full_ppr_fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank_full_ppr"))
  colnames(combined_board_qb) <- c("team","pos","player_name","full_ppr_per_gm","fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank")
  combined_board_skill <- subset(agg_skill_stats, select = c("team","pos","player_name","full_ppr_per_gm","full_ppr_fantasy_tier","full_ppr_pos_rank","consensus_pos_rank_full_ppr","consensus_ovr_rank_full_ppr"))
  colnames(combined_board_skill) <- c("team","pos","player_name","full_ppr_per_gm","fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank")
  combined_board <- rbind(combined_board_qb, combined_board_skill)
  
  combined_board$fantasy_tier <- ifelse(combined_board$pos == "RB" & combined_board$fantasy_tier<=8, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$pos == "WR" & combined_board$fantasy_tier>=8 & combined_board$fantasy_tier<=10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)

  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "De'Von Achane" & combined_board$fantasy_tier<=1, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Puka Nacua" & combined_board$fantasy_tier<=1, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Ladd McConkey" & combined_board$fantasy_tier<=2, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Christian McCaffrey" & combined_board$fantasy_tier>=3, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Derrick Henry" & combined_board$fantasy_tier<=2, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Josh Jacobs" & combined_board$fantasy_tier<=2, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Kyren Williams" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "James Cook" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Mike Evans" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Breece Hall" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 3, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Omarion Hampton" & combined_board$fantasy_tier>=4, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Davante Adams" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tyreek Hill" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tee Higgins" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Courtland Sutton" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jaxon Smith-Njigba" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Trey McBride" & combined_board$fantasy_tier<=5, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Chuba Hubbard" & combined_board$fantasy_tier<=5, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Aaron Jones" & combined_board$fantasy_tier<=5, combined_board$fantasy_tier + 3, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "DeVonta Smith" & combined_board$fantasy_tier<=5, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Joe Burrow" & combined_board$fantasy_tier<=6, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "DeVonta Smith" & combined_board$fantasy_tier<=6, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "George Pickens" & combined_board$fantasy_tier<=6, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jakobi Meyers" & combined_board$fantasy_tier<=6, combined_board$fantasy_tier + 3, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Travis Hunter" & combined_board$fantasy_tier<=6, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Matthew Golden" & combined_board$fantasy_tier<=6, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jaylen Waddle" & combined_board$fantasy_tier<=6, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "David Montgomery" & combined_board$fantasy_tier<=6, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "TreVeyon Henderson" & combined_board$fantasy_tier>=7, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Javonte Williams" & combined_board$fantasy_tier<=7, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tetairoa McMillan" & combined_board$fantasy_tier<=7, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Patrick Mahomes" & combined_board$fantasy_tier<=8, 8, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Calvin Ridley" & combined_board$fantasy_tier>=8, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "David Njoku" & combined_board$fantasy_tier<=8, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Baker Mayfield" & combined_board$fantasy_tier<=9, 9, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Brock Purdy" & combined_board$fantasy_tier<=9, 9, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Emeka Egbuka" & combined_board$fantasy_tier>=9, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Kaleb Johnson" & combined_board$fantasy_tier>=9, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Zach Charbonnet" & combined_board$fantasy_tier>=9, 8, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Ricky Pearsall" & combined_board$fantasy_tier>=9, combined_board$fantasy_tier - 3, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Chris Godwin" & combined_board$fantasy_tier>10, 8, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "T.J. Hockenson" & combined_board$fantasy_tier>=10, 9, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Mark Andrews" & combined_board$fantasy_tier>=10, 9, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tucker Kraft" & combined_board$fantasy_tier>=10, 9, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jonnu Smith" & combined_board$fantasy_tier>=10, 9, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jayden Reed" & combined_board$fantasy_tier>10, 9, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jameson Williams" & combined_board$fantasy_tier>10, 9, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Najee Harris" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jordan Mason" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Cam Skattebo" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jacorey Croskey-Merritt" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Travis Etienne" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tank Bigsby" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Bhaysul Tuten" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jaydon Blue" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Nick Chubb" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tyler Allgeier" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Brian Robinson Jr." & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Rhamondre Stevenson" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Brandon Aiyuk" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Cooper Kupp" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tory Horton" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Keon Coleman" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Isaac TeSlaa" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "KeAndre Lambert-Smith" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Elic Ayomanor" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Colston Loveland" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Pat Freiermuth" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tyler Warren" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Dalton Kincaid" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Mason Taylor" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Dallas Goedert" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jake Ferguson" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Chigoziem Okonkwo" & combined_board$fantasy_tier>10, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  
  pos_order <- c("WR" = 1, "RB" = 2, "TE" = 3, "QB" = 4)
  combined_board$sort_rank <- as.numeric(sub("^[A-Z]+", "", combined_board$pos_rank))
  combined_board <- combined_board[order(combined_board$fantasy_tier, pos_order[combined_board$pos], combined_board$sort_rank), ]
  combined_board <- combined_board[, !names(combined_board) %in% c("sort_rank")]
  
  rownames(combined_board) <- NULL
  combined_board$ovr_rank <- seq_len(nrow(combined_board))
  combined_board <- subset(combined_board, select = c("team","pos","player_name","full_ppr_per_gm","fantasy_tier","pos_rank","consensus_pos_rank", "ovr_rank","consensus_ovr_rank"))
  combined_board$diff_from_consensus <- combined_board$consensus_ovr_rank - combined_board$ovr_rank
  
  combined_board <- combined_board %>%
    mutate(pos_rank = row_number()) %>%
    group_by(pos) %>%
    mutate(pos_rank = paste0(pos, row_number())) %>%
    ungroup()
  
  write.csv(combined_board, paste0(output_path))
  
  combined_board$player_info <- paste(combined_board$player_name, combined_board$team, (paste0(as.character(combined_board$full_ppr_per_gm)," per gm")), sep = ", ")
  
  full_ppr_board <- combined_board %>%
    # Group by fantasy_tier to process each tier separately
    group_by(fantasy_tier) %>%
    # Nest the data for each tier
    nest() %>%
    # For each nested data frame, create the expanded structure
    mutate(expanded = map(data, function(df) {
      # Define all possible positions
      all_pos <- c("QB", "RB", "WR", "TE")
      
      # Split player_info by pos
      by_pos <- split(df$player_info, df$pos)
      
      # Add missing positions with empty character vectors
      for (p in all_pos) {
        if (!p %in% names(by_pos)) {
          by_pos[[p]] <- character(0)
        }
      }
      
      # Find the maximum number of players across all positions
      max_len <- max(sapply(by_pos, length))
      
      # Pad each position's player list to max_len with empty strings
      padded <- lapply(by_pos, function(players) {
        c(players, rep("", max_len - length(players)))
      })
      
      # Convert to a tibble with columns for each position
      as_tibble(padded)
    })) %>%
    # Select fantasy_tier and the expanded data, then unnest
    select(fantasy_tier, expanded) %>%
    unnest(expanded) %>%
    # Arrange by fantasy_tier (assuming it's numeric)
    arrange(as.numeric(fantasy_tier))
  
  write.csv(full_ppr_board, paste0(output_path_2))
}

build_te_premium_board <- function(agg_qb_stats, agg_skill_stats, output_path){
  combined_board_qb <- subset(agg_qb_stats, select = c("team","pos","player_name","te_premium_per_gm","te_premium_fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank_full_ppr"))
  colnames(combined_board_qb) <- c("team","pos","player_name","te_premium_per_gm","fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank")
  combined_board_skill <- subset(agg_skill_stats, select = c("team","pos","player_name","te_premium_per_gm","te_premium_fantasy_tier","full_ppr_pos_rank","consensus_pos_rank_full_ppr","consensus_ovr_rank_full_ppr"))
  colnames(combined_board_skill) <- c("team","pos","player_name","te_premium_per_gm","fantasy_tier","pos_rank","consensus_pos_rank","consensus_ovr_rank")
  combined_board <- rbind(combined_board_qb, combined_board_skill)
  
  combined_board$fantasy_tier <- ifelse(combined_board$pos == "RB", combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$pos == "TE", combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "De'Von Achane" & combined_board$fantasy_tier<=1, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Ladd McConkey" & combined_board$fantasy_tier<=2, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Christian McCaffrey" & combined_board$fantasy_tier>=3, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Ashton Jeanty" & combined_board$fantasy_tier>=3, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Lamar Jackson" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Josh Allen" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jalen Hurts" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Mike Evans" & combined_board$fantasy_tier<=3, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Breece Hall" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Davante Adams" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Tee Higgins" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Joe Burrow" & combined_board$fantasy_tier<=4, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Trey McBride" & combined_board$fantasy_tier>=5, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Jakobi Meyers" & combined_board$fantasy_tier<=5, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "TreVeyon Henderson" & combined_board$fantasy_tier>=7, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Patrick Mahomes" & combined_board$fantasy_tier<=7, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Brock Purdy" & combined_board$fantasy_tier<=7, combined_board$fantasy_tier + 2, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "Calvin Ridley" & combined_board$fantasy_tier>=8, combined_board$fantasy_tier - 1, combined_board$fantasy_tier)
  combined_board$fantasy_tier <- ifelse(combined_board$player_name == "David Njoku" & combined_board$fantasy_tier<=8, combined_board$fantasy_tier + 1, combined_board$fantasy_tier)
  
  pos_order <- c("TE" = 1, "WR" = 2, "RB" = 3, "QB" = 4)
  combined_board$sort_rank <- as.numeric(sub("^[A-Z]+", "", combined_board$pos_rank))
  combined_board <- combined_board[order(combined_board$fantasy_tier, pos_order[combined_board$pos], combined_board$sort_rank), ]
  combined_board <- combined_board[, !names(combined_board) %in% c("sort_rank")]
  
  rownames(combined_board) <- NULL
  combined_board$ovr_rank <- seq_len(nrow(combined_board))
  combined_board <- subset(combined_board, select = c("team","pos","player_name","te_premium_per_gm","fantasy_tier","pos_rank","consensus_pos_rank", "ovr_rank","consensus_ovr_rank"))
  combined_board$diff_from_consensus <- combined_board$consensus_ovr_rank - combined_board$ovr_rank
  
  combined_board <- combined_board %>%
    mutate(pos_rank = row_number()) %>%
    group_by(pos) %>%
    mutate(pos_rank = paste0(pos, row_number())) %>%
    ungroup()
  
  write.csv(combined_board, paste0(output_path))
}