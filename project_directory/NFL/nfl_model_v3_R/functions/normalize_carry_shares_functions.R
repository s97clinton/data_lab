normalize_carry_share <- function(df) {
  if (sum(df$carry_share) - 1 == 0.00) {
    # print("on target")
    
  } else if (sum(df$carry_share) - 1 < 0.00) {
    
    value <- (sum(df$carry_share) - 1)
    enhancement_share <- df$carry_share[1] + df$carry_share[2] + df$carry_share[3]
    enhancement_target <- enhancement_share - value
    scale_up <- enhancement_target/enhancement_share
    
    df$carry_share[1] <- round(df$carry_share[1] * scale_up,2)
    df$carry_share[2] <- round(df$carry_share[2] * scale_up,2)
    df$carry_share[3] <- round(df$carry_share[3] * scale_up,2)
    
    # print("low")
    # print(value)
    
  } else {
    
    value <- (sum(df$carry_share) - 1)
    if (rb1 == TRUE) {
      unprotected_share <- df$carry_share[2] + df$carry_share[3]
      unprotected_share_target <- unprotected_share - value
      scale_down <- unprotected_share_target/unprotected_share
      df$carry_share[2] <- round(df$carry_share[2] * scale_down,2)
      df$carry_share[3] <- round(df$carry_share[3] * scale_down,2)
    } else {
      unprotected_share <- df$carry_share[1] + df$carry_share[2] + df$carry_share[3]
      unprotected_share_target <- unprotected_share - value
      scale_down <- unprotected_share_target/unprotected_share
      df$carry_share[1] <- round(df$carry_share[1] * scale_down,2)
      df$carry_share[2] <- round(df$carry_share[2] * scale_down,2)
      df$carry_share[3] <- round(df$carry_share[3] * scale_down,2)
    }
    
    # print("high")
    # print(value)
    
  }
  return (df)
}

normalize_td_share <- function(df) {
  if (sum(df$rush_td_share) - 1 == 0.00) {
    # print("on target")
    
  } else if (sum(df$rush_td_share) - 1 < 0.00) {
    
    value <- (sum(df$rush_td_share) - 1)
    enhancement_share <- df$rush_td_share[1] + df$rush_td_share[2] + df$rush_td_share[3]
    enhancement_target <- enhancement_share - value
    scale_up <- enhancement_target/enhancement_share
    
    df$rush_td_share[1] <- round(df$rush_td_share[1] * scale_up,2)
    df$rush_td_share[2] <- round(df$rush_td_share[2] * scale_up,2)
    df$rush_td_share[3] <- round(df$rush_td_share[3] * scale_up,2)

    # print("low")
    # print(value)
    
  } else {
    
    value <- (sum(df$rush_td_share) - 1)
    if (rb1 == TRUE) {
      unprotected_share <- df$rush_td_share[2] + df$rush_td_share[3]
      unprotected_share_target <- unprotected_share - value
      scale_down <- unprotected_share_target/unprotected_share
      df$rush_td_share[2] <- round(df$rush_td_share[2] * scale_down,2)
      df$rush_td_share[3] <- round(df$rush_td_share[3] * scale_down,2)
    } else {
      unprotected_share <- df$rush_td_share[1] + df$rush_td_share[2] + df$rush_td_share[3]
      unprotected_share_target <- unprotected_share - value
      scale_down <- unprotected_share_target/unprotected_share
      df$rush_td_share[1] <- round(df$rush_td_share[1] * scale_down,2)
      df$rush_td_share[2] <- round(df$rush_td_share[2] * scale_down,2)
      df$rush_td_share[3] <- round(df$rush_td_share[3] * scale_down,2)
    }
    # print("high")
    # print(value)
    
  }
  return (df)
}

normalize_team_carry_share <- function(df) {
  df$yards_per_carry <- ifelse(df$yards_per_carry < 1.00, 1.00, df$yards_per_carry)
  df$yards_per_carry <- ifelse(df$yards_per_carry < 2.50 & df$pos != 'QB', 2.50, df$yards_per_carry)
  df$yards_per_carry <- ifelse(df$yards_per_carry > 6.50, 6.50, df$yards_per_carry)
  
  df$carry_share <- ifelse(df$carry_share < 0.01, 0.01, df$carry_share)
  df$rush_td_share <- ifelse(df$rush_td_share < 0.01, 0.01, df$rush_td_share)
  
  df <- normalize_carry_share(df)
  df <- normalize_td_share(df)
  
  return (df)
}