from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, log_loss
import pandas as pd


def multinomial_logistic_regression(train_set, test_set, features, target, one_hot_features=None, ordinal_features=None, solver='lbfgs', max_iter=1000, test_set_target=False):
    """
    Function:
    -This function will use sklearn to train a multinomial logistic regression model on the <train_set> before
    running inferences on the <test_set> and returning the output along with a variety of model evaluation
    metrics.

    Parameters:
    <train_set> (Pandas Dataframe): Dataframe containing the features and target variable for use in
    modeling.
    <test_set> (Pandas Dataframe): Dataframe containing the features for use in inference.
    <features> (List): A list containing the features used in modeling.
    <target> (One Item List): A list containing the target feature. (one-item list)
    <one_hot_features>: List of categorical features that require one-hot encoding.
    <solver>: Choice of solver for multinomial_logistic; defaults to 'lbfgs'.
    <max_iter>: Value to set max_iter in modeling process; default is 1000.
    <test_set_target> (Boolean): A Boolean indicating whether or not we have the output for the test set. (impacts returned values)
    
    Returns:
    <model>: A scikit-learn model object.
    <x_test>: The test set features.
    <y_pred>: Predicted class labels for the test set.
    <y_prob>: Predicted probabilities for the test set.

    if <test_set_target> == TRUE, also returns:
        - <y_test>: The test set target.
        - <classification_report>: The scikit-learn classification report for the test set.
        - <log_loss_score>: The log loss for the test set (useful for multi-class classification).
    """
    x_train = train_set[features]
    y_train = train_set[target].values.ravel()
    x_test = test_set[features]
    if test_set_target == True:
        y_test = test_set[target].values.ravel()

    feature_transformers = []

    if one_hot_features:
        feature_transformers.append(('onehot', OneHotEncoder(), one_hot_features))
    if ordinal_features:
        feature_transformers.append(('ordinal', OrdinalEncoder(), ordinal_features))

    pre_processor = ColumnTransformer(
        transformers = feature_transformers,
        remainder="passthrough"
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', pre_processor),
        ('model', LogisticRegression(solver=solver, max_iter=max_iter))
    ])

    pipeline.fit(x_train, y_train)

    y_pred = pipeline.predict(x_test)
    y_prob = pipeline.predict_proba(x_test)
    class_labels = pipeline.named_steps['model'].classes_
    y_prob_df = pd.DataFrame(y_prob, columns=[f'{label}' for label in class_labels])

    test_output = pd.concat([test_set, y_prob_df], axis=1)

    if test_set_target == True:
        report = classification_report(y_test, y_pred, zero_division=0)
        log_loss_score = log_loss(y_test, y_prob)

        return test_output, x_test, y_pred, y_prob, pipeline, y_test, report, log_loss_score
    
    else:
        return test_output, x_test, y_pred, y_prob_df

    

