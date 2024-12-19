import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix


def generate_model_report(l_y_test: dict, l_y_pred_log: dict, l_y_pred_rf: dict, threshold: float = 0.5) -> pd.DataFrame:
    """
    Generate a report for each version and model containing precision, recall, f1-score, support, and accuracy.

    Parameters:
    - l_y_test (dict): A dictionary with versions as keys and true labels as values.
    - l_y_pred_log (dict): A dictionary with versions as keys and Logistic Regression predicted probabilities as values.
    - l_y_pred_rf (dict): A dictionary with versions as keys and Random Forest predicted probabilities as values.
    - threshold (float): Threshold to convert predicted probabilities into binary classifications (default: 0.5).

    Returns:
    - pd.DataFrame: DataFrame with all metrics for each model and version.
    """
    report_data = []

    # Versions to iterate through
    versions = list(l_y_test.keys())

    for key in versions:
        # Convert probabilities to binary predictions using the threshold
        y_pred_log_binary = [1 if prob >= threshold else 0 for prob in l_y_pred_log[key]]
        y_pred_rf_binary = [1 if prob >= threshold else 0 for prob in l_y_pred_rf[key]]

        # Logistic Regression metrics
        precision_log_0 = precision_score(l_y_test[key], y_pred_log_binary, pos_label=0)
        precision_log_1 = precision_score(l_y_test[key], y_pred_log_binary, pos_label=1)
        recall_log_0 = recall_score(l_y_test[key], y_pred_log_binary, pos_label=0)
        recall_log_1 = recall_score(l_y_test[key], y_pred_log_binary, pos_label=1)
        f1_log_0 = f1_score(l_y_test[key], y_pred_log_binary, pos_label=0)
        f1_log_1 = f1_score(l_y_test[key], y_pred_log_binary, pos_label=1)
        accuracy_log = accuracy_score(l_y_test[key], y_pred_log_binary)
        support_log_0, support_log_1 = confusion_matrix(l_y_test[key], y_pred_log_binary).sum(axis=0)

        # Random Forest metrics
        precision_rf_0 = precision_score(l_y_test[key], y_pred_rf_binary, pos_label=0)
        precision_rf_1 = precision_score(l_y_test[key], y_pred_rf_binary, pos_label=1)
        recall_rf_0 = recall_score(l_y_test[key], y_pred_rf_binary, pos_label=0)
        recall_rf_1 = recall_score(l_y_test[key], y_pred_rf_binary, pos_label=1)
        f1_rf_0 = f1_score(l_y_test[key], y_pred_rf_binary, pos_label=0)
        f1_rf_1 = f1_score(l_y_test[key], y_pred_rf_binary, pos_label=1)
        accuracy_rf = accuracy_score(l_y_test[key], y_pred_rf_binary)
        support_rf_0, support_rf_1 = confusion_matrix(l_y_test[key], y_pred_rf_binary).sum(axis=0)

        # Append data to the report
        report_data.append({
            "Version": key,
            "Model": "Logistic Regression",
            "Precision 0": precision_log_0,
            "Precision 1": precision_log_1,
            "Recall 0": recall_log_0,
            "Recall 1": recall_log_1,
        })

        report_data.append({
            "Version": key,
            "Model": "Random Forest",
            "Precision 0": precision_rf_0,
            "Precision 1": precision_rf_1,
            "Recall 0": recall_rf_0,
            "Recall 1": recall_rf_1,
        })

    # Create the DataFrame
    df_report = pd.DataFrame(report_data)
    return df_report
