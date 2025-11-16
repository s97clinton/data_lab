def cnvt_deci_to_prob(decimal_odds: float) -> float:
    """Function: Convert decimal odds to float."""
    probability = 1/decimal_odds
    return probability