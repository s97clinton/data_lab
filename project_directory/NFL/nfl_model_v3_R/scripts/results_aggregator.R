source("functions/calculate_game_stats.R")
source("functions/build_fantasy_boards.R")

prep_consensus_qb_to_merge("data_files/consensus_board/no_ppr_consensus_rankings.csv", "data_files/consensus_board/half_ppr_consensus_rankings.csv", "data_files/consensus_board/full_ppr_consensus_rankings.csv", "data_files/consensus_board/consensus_qb_board.csv")
prep_consensus_skill_to_merge("data_files/consensus_board/no_ppr_consensus_rankings.csv", "data_files/consensus_board/half_ppr_consensus_rankings.csv", "data_files/consensus_board/full_ppr_consensus_rankings.csv", "data_files/consensus_board/consensus_skill_board.csv")

aggregate_season_outcomes("result_dump/projected_weekly_game_outcomes/", "result_dump/season_results.csv")
aggregate_team_season_stats("result_dump/projected_fantasy_stats/projected_team_fantasy/", "result_dump/projected_fantasy_stats/team_season_data.csv")

agg_qb_stats <- aggregate_qb_season_stats("result_dump/projected_fantasy_stats/qb_board/", "data_files/consensus_board/consensus_qb_board.csv", "result_dump/projected_fantasy_stats/qb_board_season_results.csv")
agg_skill_stats <- aggregate_skill_season_stats("result_dump/projected_fantasy_stats/skill_board/", "data_files/consensus_board/consensus_skill_board.csv", "result_dump/projected_fantasy_stats/skill_board_season_results.csv")

build_no_ppr_board(agg_qb_stats, agg_skill_stats, "result_dump/fantasy_boards/no_ppr_combined_board.csv")
build_half_ppr_board(agg_qb_stats, agg_skill_stats, "result_dump/fantasy_boards/half_ppr_combined_board.csv")
build_full_ppr_board(agg_qb_stats, agg_skill_stats, "result_dump/fantasy_boards/full_ppr_stacked_board.csv", "result_dump/fantasy_boards/full_ppr_draft_board.csv")
build_te_premium_board(agg_qb_stats, agg_skill_stats, "result_dump/fantasy_boards/te_premium_combined_board.csv")

