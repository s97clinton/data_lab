
def drive_multinomial_results_to_drive_outcome(model_test_output):
    """
    Function:
    -Transform output of multinomial logistic regression model into 
    NFL spread and total.

    Parameters:
    <model_test_output> (Pandas Dataframe): Dataframe with output of projections
    from multinomial logistic regression model to transform into points per drive
    for each offense in NFL game

    Returns:
    <game_projections> (Pandas Dataframe): Dataframe with projected points per drive
    for offense.
    """
    model_test_output['points_per_drive'] = (model_test_output['fg_made']*3) + (model_test_output['touchdown']*7)
    model_test_output = model_test_output[['season','week','off','def','venue','points_per_drive']]

    return model_test_output

