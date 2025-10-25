source("functions/qb_stat_functions.R")

proj_df$away_qb <- ''
proj_df$home_qb <- ''
proj_df$away_qb_int_rate <- 0.0
proj_df$home_qb_int_rate <- 0.0
proj_df$away_qb_sack_rate <- 0.0
proj_df$home_qb_sack_rate <- 0.0

source("scripts/set_qb_rates/ARI.R")
source("scripts/set_qb_rates/ATL.R")
source("scripts/set_qb_rates/BAL.R")
source("scripts/set_qb_rates/BUF.R")
source("scripts/set_qb_rates/CAR.R")
source("scripts/set_qb_rates/CHI.R")
source("scripts/set_qb_rates/CIN.R")
source("scripts/set_qb_rates/CLE.R")
source("scripts/set_qb_rates/DAL.R")
source("scripts/set_qb_rates/DEN.R")
source("scripts/set_qb_rates/DET.R")
source("scripts/set_qb_rates/GB.R")
source("scripts/set_qb_rates/HOU.R")
source("scripts/set_qb_rates/IND.R")
source("scripts/set_qb_rates/JAX.R")
source("scripts/set_qb_rates/KC.R")
source("scripts/set_qb_rates/LAC.R")
source("scripts/set_qb_rates/LAR.R")
source("scripts/set_qb_rates/LVR.R")
source("scripts/set_qb_rates/MIA.R")
source("scripts/set_qb_rates/MIN.R")
source("scripts/set_qb_rates/NE.R")
source("scripts/set_qb_rates/NO.R")
source("scripts/set_qb_rates/NYG.R")
source("scripts/set_qb_rates/NYJ.R")
source("scripts/set_qb_rates/PHI.R")
source("scripts/set_qb_rates/PIT.R")
source("scripts/set_qb_rates/SF.R")
source("scripts/set_qb_rates/SEA.R")
source("scripts/set_qb_rates/TB.R")
source("scripts/set_qb_rates/TEN.R")
source("scripts/set_qb_rates/WSH.R")

rm(set_qb_int_sack_rates,set_team_qb)