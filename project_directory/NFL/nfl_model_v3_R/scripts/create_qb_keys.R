library(hash)
impact_players <- hash()

#########
#ARIZONA
#########
impact_players[["ari_kyler_murray"]] <- ifelse(model_params$injuries=='yes',1,1)
#########
#ATLANTA
#########
impact_players[["atl_michael_penix"]] <- ifelse(model_params$injuries=='yes',1,1)
##########
#BALTIMORE
##########
impact_players[["bal_lamar_jackson"]] <- ifelse(model_params$injuries=='yes',1,1)
##########
#BUFFALO
##########
impact_players[["buf_josh_allen"]] <- ifelse(model_params$injuries=='yes',1,1)
##########
#CAROLINA
##########
impact_players[["car_bryce_young"]] <- ifelse(model_params$injuries=='yes',1,1) 
##########
#CHICAGO
########## 
impact_players[["chi_caleb_williams"]] <- ifelse(model_params$injuries=='yes',1,1)
##########
#CINCY
##########
impact_players[["cin_joe_burrow"]] <- ifelse(model_params$injuries=='yes',1,1)
##########
#CLEVELAND
##########
impact_players[["cle_joe_flacco"]] <- ifelse(model_params$injuries=='yes',1,1)
##########
#DALLAS
##########
impact_players[["dal_dak_prescott"]] <- ifelse(model_params$injuries=='yes',1,1)
##########
#DENVER
##########
impact_players[["den_bo_nix"]] <- ifelse(model_params$injuries=='yes',1,1)
##########
#DETROIT
##########
impact_players[["det_jared_goff"]] <- ifelse(model_params$injuries=='yes',1,1)
###########
#GREEN BAY
###########
impact_players[["gb_jordan_love"]] <- ifelse(model_params$injuries=='yes',1,1)
##########
#HOUSTON
##########
impact_players[["hou_cj_stroud"]] <- ifelse(model_params$injuries=='yes',1,1)
##########
#INDY
##########
impact_players[["ind_daniel_jones"]] <- ifelse(model_params$injuries=='yes',1,1)
#############
#JACKSONVILLE
#############
impact_players[["jax_trevor_lawrence"]] <- ifelse(model_params$injuries=='yes',1,1)
#############
#KANSAS CITY
#############
impact_players[["kc_pat_mahomes"]] <- ifelse(model_params$injuries=='yes',1,1)
############
#LA CHARGERS
############
impact_players[["lac_justin_herbert"]] <- ifelse(model_params$injuries=='yes',1,1)
############
#LA RAMS
############
impact_players[["lar_matt_stafford"]] <- ifelse(model_params$injuries=='yes',1,1) 
###########
#LAS VEGAS
###########
impact_players[["lvr_geno_smith"]] <- ifelse(model_params$injuries=='yes',1,1)
############
#MIAMI
############
impact_players[["mia_tua_tagovailoa"]] <- ifelse(model_params$injuries=='yes',1,1)
############
#MINNESOTA
############
impact_players[["min_jj_mccarthy"]] <- ifelse(model_params$injuries=='yes',1,1)
############
#NEW ENGLAND
############
impact_players[["ne_drake_maye"]] <- ifelse(model_params$injuries=='yes',1,1)
############
#NEW ORLEANS
############
impact_players[["no_spencer_rattler"]] <- ifelse(model_params$injuries=='yes',1,1)
###################
#NEW YORK GIANTS
###################
impact_players[["nyg_russell_wilson"]] <- ifelse(model_params$injuries=='yes',1,1)
###################
#NEW YORK JETS
###################
impact_players[["nyj_justin_fields"]] <- ifelse(model_params$injuries=='yes',1,1)
###############
#PHILADELPHIA
###############
impact_players[["phi_jalen_hurts"]] <- ifelse(model_params$injuries=='yes',1,1)
###############
#PITTSBURGH
###############
impact_players[["pit_aaron_rodgers"]] <- ifelse(model_params$injuries=='yes',1,1)
###############
#SEATTLE
###############
impact_players[["sea_sam_darnold"]] <- ifelse(model_params$injuries=='yes',1,1)
###############
#SF 49ers
###############
impact_players[["sf_brock_purdy"]] <- ifelse(model_params$injuries=='yes',1,1)
###############
#TAMPA BAY
###############
impact_players[["tb_baker_mayfield"]] <- ifelse(model_params$injuries=='yes',1,1)
###############
#TENNESSEE
###############
impact_players[["ten_cam_ward"]] <- ifelse(model_params$injuries=='yes',1,1)
###############
#WASHINGTON
###############
impact_players[["wsh_jayden_daniels"]] <- ifelse(model_params$injuries=='yes',1,1)

