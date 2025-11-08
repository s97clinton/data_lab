from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, log_loss
import pandas as pd
from typing import List, Optional

def build_multinomial_log_reg_pipeline(train_set: pd.DataFrame,
                                       target: str,
                                       numeric_features: Optional[List[str]] = [],
                                       one_hot_features: Optional[List[str]] = [],
                                       ordinal_features: Optional[List[str]] = [],
                                       other_features: Optional[List[str]] = [],
                                       solver: str = 'lbfgs',
                                       max_iter: int = 10000) -> Pipeline:
    """
    -This function will build and fit a multinomial logistic regression pipeline and return the pipeline.

    Parameters:
    <train_set> (Pandas Dataframe): Dataframe containing the features and target variable for use in
    modeling.
    <target> (String): Name of the target feature.
    <numeric_features> (List): Numeric features to scale using StandardScaler().
    <one_hot_features> (List): Categorical features to one-hot encode.
    <ordinal_features> (List): Categorical features to ordial encode.
    <other_features> (List): Features to pass in without scaling/encoding.
    <solver> (str): Solver for LogisticRegression, must support multinomial, options: {'lbfgs'(default), 'newton-cg', 'sag', 'saga', 'newton-cholesky'}
    <max_iter> (int): Maximum number of iterations for the solver; default is 10000.
    
    Returns:
    Pipeline: Fitted scikit-learn Pipeline ready for prediction on new data.

    Raises:
    ValueError: If invalid solver, missing columns, or overlapping features.
    """
    features = numeric_features + one_hot_features + ordinal_features + other_features
    if not features:
        raise ValueError("Feature Lists are all empty; you need to enter at least one feature.")
    if len(set(features)) != len(features):
        raise ValueError("Feature Lists Contain Overlapping Column Names.")
    
    missing_cols = [col for col in features + [target] if col not in train_set.columns]
    if missing_cols:
        raise ValueError(f"Columns not found in train_set DataFrame: {missing_cols}")
    
    valid_solvers = ['lbfgs', 'newton-cg', 'sag', 'saga', 'newton-cholesky']
    if solver not in valid_solvers:
        raise ValueError(f"Solver must be one of {valid_solvers}, value passed: {solver}")

    transformers = []
    if numeric_features:
        transformers.append(('numeric', StandardScaler(), numeric_features))
    if one_hot_features:
        transformers.append(('onehot', OneHotEncoder(handle_unknown='ignore'), one_hot_features))
    if ordinal_features:
        transformers.append(('ordinal', OrdinalEncoder(handle_unknown=-1), ordinal_features))
    if other_features:
        transformers.append(('passthrough', 'passthrough', other_features))

    pre_processor = ColumnTransformer(
        transformers = transformers,
        remainder="drop"
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', pre_processor),
        ('model', LogisticRegression(solver=solver, max_iter=max_iter))
    ])

    pipeline.fit(train_set[features], train_set[target])

    return pipeline


def project_multinomial_test_set(pipeline: Pipeline, test_set: pd.DataFrame, target: str, target_in_test_set: bool) -> pd.DataFrame:
    """
    Function:
    -Takes sci-kit-learn multinomial <Pipeline> and <test_set> Pandas DataFrame; runs the
    Pipeline .predict() and .predict_proba() and attaches projections to the <test_set> df to return.

    Parameters:
    <pipeline> (Pipeline): sci-kit-learn multinomial pipeline.
    <test_set> (DataFrame): Test Data.
    <target> (String): Name of target column.
    <future_projection> (bool): True/False on whether projected target has occurred.

    Returns:
    <result_df> (DataFrame): Model Projections attached to original <test_set>.
    """
    x_test = test_set.copy()
    if target_in_test_set:
        x_test = x_test.drop(columns=[target])

    y_pred = pipeline.predict(x_test)
    y_pred_df = pd.Series(y_pred, name='prediction', index=x_test.index)

    y_prob = pipeline.predict_proba(x_test)
    class_names = pipeline.classes_
    prob_cols = [f'prob_{name}' for name in class_names]
    y_prob_df = pd.DataFrame(y_prob, columns=prob_cols, index=x_test.index)

    result_df = pd.concat([x_test, y_prob_df, y_pred_df], axis=1)

    return result_df

def create_multinomial_metrics_report(pipeline: Pipeline, test_set: pd.DataFrame, target: str):
    """
    Function:
    -Takes sci-kit-learn multinomial <Pipeline> and <test_set> Pandas DataFrame; runs the
    Pipeline .predict() and .predict_proba() and attaches projections to the <test_set> df to return.

    Parameters:
    <pipeline> (Pipeline): sci-kit-learn multinomial pipeline.
    <test_set> (DataFrame): Test Data.
    <target> (String): Name of target column.

    Returns:
    <classification_results_report>
    <log_loss_score>
    """
    y_pred = pipeline.predict(test_set)
    y_prob = pipeline.predict_proba(test_set)
    y_test = test_set[target]
    classification_results_report = classification_report(y_test, y_pred, zero_division=0)
    log_loss_score = log_loss(y_test, y_prob)
    
    return classification_results_report, log_loss_score