normalize_tgt_share <- function(df) {
  if (sum(df$tgt_share) - 1 == 0.00) {
    # print("on target")
    
  } else if (sum(df$tgt_share) - 1 < 0.00) {
    
    value <- (sum(df$tgt_share) - 1)
    if (wr1 == TRUE & wr1a == TRUE){
      enhancement_share <- df$tgt_share[1] + df$tgt_share[2] + df$tgt_share[3] + df$tgt_share[4] + df$tgt_share[5]
      enhancement_target <- enhancement_share - value
      scale_up <- enhancement_target/enhancement_share
      df$tgt_share[1] <- round(df$tgt_share[1] * scale_up,2)
      df$tgt_share[2] <- round(df$tgt_share[2] * scale_up,2)
      df$tgt_share[3] <- round(df$tgt_share[3] * scale_up,2)
      df$tgt_share[4] <- round(df$tgt_share[4] * scale_up,2)
      df$tgt_share[5] <- round(df$tgt_share[5] * scale_up,2)
    } else if (wr1 == TRUE & wr1a == FALSE){
      enhancement_share <- df$tgt_share[1] + df$tgt_share[2] + df$tgt_share[3] + df$tgt_share[4] + df$tgt_share[5] + df$tgt_share[6]
      enhancement_target <- enhancement_share - value
      scale_up <- enhancement_target/enhancement_share
      df$tgt_share[1] <- round(df$tgt_share[1] * scale_up,2)
      df$tgt_share[2] <- round(df$tgt_share[2] * scale_up,2)
      df$tgt_share[3] <- round(df$tgt_share[3] * scale_up,2)
      df$tgt_share[4] <- round(df$tgt_share[4] * scale_up,2)
      df$tgt_share[5] <- round(df$tgt_share[5] * scale_up,2)
      df$tgt_share[6] <- round(df$tgt_share[6] * scale_up,2)
    } else {
      enhancement_share <- df$tgt_share[1] + df$tgt_share[2] + df$tgt_share[3] + df$tgt_share[4] + df$tgt_share[5] + df$tgt_share[6] + df$tgt_share[7]
      enhancement_target <- enhancement_share - value
      scale_up <- enhancement_target/enhancement_share
      df$tgt_share[1] <- round(df$tgt_share[1] * scale_up,2)
      df$tgt_share[2] <- round(df$tgt_share[2] * scale_up,2)
      df$tgt_share[3] <- round(df$tgt_share[3] * scale_up,2)
      df$tgt_share[4] <- round(df$tgt_share[4] * scale_up,2)
      df$tgt_share[5] <- round(df$tgt_share[5] * scale_up,2)
      df$tgt_share[6] <- round(df$tgt_share[6] * scale_up,2)
      df$tgt_share[7] <- round(df$tgt_share[7] * scale_up,2)
    }
    # print("low")
    # print(value)
    
  } else {
    
    value <- (sum(df$tgt_share) - 1)
    if (wr1 == FALSE & wr1a == FALSE){
      unprotected_share <- df$tgt_share[1] + df$tgt_share[2] + df$tgt_share[3] + df$tgt_share[4] + df$tgt_share[5] + df$tgt_share[6] + df$tgt_share[7] + df$tgt_share[8] + df$tgt_share[9] + df$tgt_share[10]
      unprotected_share_target <- unprotected_share - value
      scale_down <- unprotected_share_target/unprotected_share
      df$tgt_share[1] <- round(df$tgt_share[1] * scale_down,2)
      df$tgt_share[2] <- round(df$tgt_share[2] * scale_down,2)
      df$tgt_share[3] <- round(df$tgt_share[3] * scale_down,2)
      df$tgt_share[4] <- round(df$tgt_share[4] * scale_down,2)
      df$tgt_share[5] <- round(df$tgt_share[5] * scale_down,2)
      df$tgt_share[6] <- round(df$tgt_share[6] * scale_down,2)
      df$tgt_share[7] <- round(df$tgt_share[7] * scale_down,2)
      df$tgt_share[8] <- round(df$tgt_share[8] * scale_down,2)
      df$tgt_share[9] <- round(df$tgt_share[9] * scale_down,2)
      df$tgt_share[10] <- round(df$tgt_share[10] * scale_down,2)     
    } else if (wr1 == TRUE & wr1a == FALSE){
      unprotected_share <- df$tgt_share[2] + df$tgt_share[3] + df$tgt_share[4] + df$tgt_share[5] + df$tgt_share[6] + df$tgt_share[7] + df$tgt_share[8] + df$tgt_share[9] + df$tgt_share[10]
      unprotected_share_target <- unprotected_share - value
      scale_down <- unprotected_share_target/unprotected_share
      df$tgt_share[2] <- round(df$tgt_share[2] * scale_down,2)
      df$tgt_share[3] <- round(df$tgt_share[3] * scale_down,2)
      df$tgt_share[4] <- round(df$tgt_share[4] * scale_down,2)
      df$tgt_share[5] <- round(df$tgt_share[5] * scale_down,2)
      df$tgt_share[6] <- round(df$tgt_share[6] * scale_down,2)
      df$tgt_share[7] <- round(df$tgt_share[7] * scale_down,2)
      df$tgt_share[8] <- round(df$tgt_share[8] * scale_down,2)
      df$tgt_share[9] <- round(df$tgt_share[9] * scale_down,2)
      df$tgt_share[10] <- round(df$tgt_share[10] * scale_down,2)    
    } else {
      unprotected_share <- df$tgt_share[3] + df$tgt_share[4] + df$tgt_share[5] + df$tgt_share[6] + df$tgt_share[7] + df$tgt_share[8] + df$tgt_share[9] + df$tgt_share[10]
      unprotected_share_target <- unprotected_share - value
      scale_down <- unprotected_share_target/unprotected_share
      df$tgt_share[3] <- round(df$tgt_share[3] * scale_down,2)
      df$tgt_share[4] <- round(df$tgt_share[4] * scale_down,2)
      df$tgt_share[5] <- round(df$tgt_share[5] * scale_down,2)
      df$tgt_share[6] <- round(df$tgt_share[6] * scale_down,2)
      df$tgt_share[7] <- round(df$tgt_share[7] * scale_down,2)
      df$tgt_share[8] <- round(df$tgt_share[8] * scale_down,2)
      df$tgt_share[9] <- round(df$tgt_share[9] * scale_down,2)
      df$tgt_share[10] <- round(df$tgt_share[10] * scale_down,2)
    }
    # print("high")
    # print(value)
    
  }
  
  return (df)
}

normalize_td_share <- function(df) {
  if (sum(df$rec_td_share) - 1 == 0.00) {
    # print("on target")
    
  } else if (sum(df$rec_td_share) - 1 < 0.00) {
    
    value <- (sum(df$rec_td_share) - 1)
    if (wr1 == TRUE & wr1a == TRUE){
      enhancement_share <- df$rec_td_share[1] + df$rec_td_share[2] + df$rec_td_share[3] + df$rec_td_share[4] + df$rec_td_share[5]
      enhancement_target <- enhancement_share - value
      scale_up <- enhancement_target/enhancement_share
      df$rec_td_share[1] <- round(df$rec_td_share[1] * scale_up,2)
      df$rec_td_share[2] <- round(df$rec_td_share[2] * scale_up,2)
      df$rec_td_share[3] <- round(df$rec_td_share[3] * scale_up,2)
      df$rec_td_share[4] <- round(df$rec_td_share[4] * scale_up,2)
      df$rec_td_share[5] <- round(df$rec_td_share[5] * scale_up,2)
    } else if (wr1 == TRUE & wr1a == FALSE){
      enhancement_share <- df$rec_td_share[1] + df$rec_td_share[2] + df$rec_td_share[3] + df$rec_td_share[4] + df$rec_td_share[5] + df$rec_td_share[6]
      enhancement_target <- enhancement_share - value
      scale_up <- enhancement_target/enhancement_share
      df$rec_td_share[1] <- round(df$rec_td_share[1] * scale_up,2)
      df$rec_td_share[2] <- round(df$rec_td_share[2] * scale_up,2)
      df$rec_td_share[3] <- round(df$rec_td_share[3] * scale_up,2)
      df$rec_td_share[4] <- round(df$rec_td_share[4] * scale_up,2)
      df$rec_td_share[5] <- round(df$rec_td_share[5] * scale_up,2)
      df$rec_td_share[6] <- round(df$rec_td_share[6] * scale_up,2)
    } else {
      enhancement_share <- df$rec_td_share[1] + df$rec_td_share[2] + df$rec_td_share[3] + df$rec_td_share[4] + df$rec_td_share[5] + df$rec_td_share[6] + df$rec_td_share[7]
      enhancement_target <- enhancement_share - value
      scale_up <- enhancement_target/enhancement_share
      df$rec_td_share[1] <- round(df$rec_td_share[1] * scale_up,2)
      df$rec_td_share[2] <- round(df$rec_td_share[2] * scale_up,2)
      df$rec_td_share[3] <- round(df$rec_td_share[3] * scale_up,2)
      df$rec_td_share[4] <- round(df$rec_td_share[4] * scale_up,2)
      df$rec_td_share[5] <- round(df$rec_td_share[5] * scale_up,2)
      df$rec_td_share[6] <- round(df$rec_td_share[6] * scale_up,2)
      df$rec_td_share[7] <- round(df$rec_td_share[7] * scale_up,2)
    }
    # print("low")
    # print(value)
    
  } else {
    
    value <- (sum(df$rec_td_share) - 1)
    if (wr1 == FALSE & wr1a == FALSE){
      unprotected_share <- df$rec_td_share[1] + df$rec_td_share[2] + df$rec_td_share[3] + df$rec_td_share[4] + df$rec_td_share[5] + df$rec_td_share[6] + df$rec_td_share[7] + df$rec_td_share[8] + df$rec_td_share[9] + df$rec_td_share[10]
      unprotected_share_target <- unprotected_share - value
      scale_down <- unprotected_share_target/unprotected_share
      df$rec_td_share[1] <- round(df$rec_td_share[1] * scale_down,2)
      df$rec_td_share[2] <- round(df$rec_td_share[2] * scale_down,2)
      df$rec_td_share[3] <- round(df$rec_td_share[3] * scale_down,2)
      df$rec_td_share[4] <- round(df$rec_td_share[4] * scale_down,2)
      df$rec_td_share[5] <- round(df$rec_td_share[5] * scale_down,2)
      df$rec_td_share[6] <- round(df$rec_td_share[6] * scale_down,2)
      df$rec_td_share[7] <- round(df$rec_td_share[7] * scale_down,2)
      df$rec_td_share[8] <- round(df$rec_td_share[8] * scale_down,2)
      df$rec_td_share[9] <- round(df$rec_td_share[9] * scale_down,2)
      df$rec_td_share[10] <- round(df$rec_td_share[10] * scale_down,2)     
    } else if (wr1 == TRUE & wr1a == FALSE){
      unprotected_share <- df$rec_td_share[2] + df$rec_td_share[3] + df$rec_td_share[4] + df$rec_td_share[5] + df$rec_td_share[6] + df$rec_td_share[7] + df$rec_td_share[8] + df$rec_td_share[9] + df$rec_td_share[10]
      unprotected_share_target <- unprotected_share - value
      scale_down <- unprotected_share_target/unprotected_share
      df$rec_td_share[2] <- round(df$rec_td_share[2] * scale_down,2)
      df$rec_td_share[3] <- round(df$rec_td_share[3] * scale_down,2)
      df$rec_td_share[4] <- round(df$rec_td_share[4] * scale_down,2)
      df$rec_td_share[5] <- round(df$rec_td_share[5] * scale_down,2)
      df$rec_td_share[6] <- round(df$rec_td_share[6] * scale_down,2)
      df$rec_td_share[7] <- round(df$rec_td_share[7] * scale_down,2)
      df$rec_td_share[8] <- round(df$rec_td_share[8] * scale_down,2)
      df$rec_td_share[9] <- round(df$rec_td_share[9] * scale_down,2)
      df$rec_td_share[10] <- round(df$rec_td_share[10] * scale_down,2)    
    } else {
      unprotected_share <- df$rec_td_share[3] + df$rec_td_share[4] + df$rec_td_share[5] + df$rec_td_share[6] + df$rec_td_share[7] + df$rec_td_share[8] + df$rec_td_share[9] + df$rec_td_share[10]
      unprotected_share_target <- unprotected_share - value
      scale_down <- unprotected_share_target/unprotected_share
      df$rec_td_share[3] <- round(df$rec_td_share[3] * scale_down,2)
      df$rec_td_share[4] <- round(df$rec_td_share[4] * scale_down,2)
      df$rec_td_share[5] <- round(df$rec_td_share[5] * scale_down,2)
      df$rec_td_share[6] <- round(df$rec_td_share[6] * scale_down,2)
      df$rec_td_share[7] <- round(df$rec_td_share[7] * scale_down,2)
      df$rec_td_share[8] <- round(df$rec_td_share[8] * scale_down,2)
      df$rec_td_share[9] <- round(df$rec_td_share[9] * scale_down,2)
      df$rec_td_share[10] <- round(df$rec_td_share[10] * scale_down,2)
    }
    # print("high")
    # print(value)
    
  }
  
  return (df)
}

normalize_team_target_share <- function(df) {
  
  df$tgt_share <- ifelse(df$tgt_share < 0.01, 0.01, df$tgt_share)
  df$rec_td_share <- ifelse(df$rec_td_share < 0.01, 0.01, df$rec_td_share)
  
  df <- normalize_tgt_share(df)
  df <- normalize_td_share(df)
  
  return (df)
}