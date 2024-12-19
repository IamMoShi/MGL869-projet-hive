import matplotlib.pyplot as plt
from sklearn.metrics import precision_score


def plot_precision(l_y_test: dict, l_y_pred_log: dict, l_y_pred_rf: dict, threshold: float = 0.5) -> None:
    """
    Plot precision scores for classes 0 and 1 for Logistic Regression and Random Forest across versions.

    Parameters:
    - l_y_test (dict): A dictionary with versions as keys and true labels as values.
    - l_y_pred_log (dict): A dictionary with versions as keys and Logistic Regression predicted probabilities as values.
    - l_y_pred_rf (dict): A dictionary with versions as keys and Random Forest predicted probabilities as values.
    - threshold (float): Threshold to convert predicted probabilities into binary classifications (default: 0.5).
    """
    # Initialize lists to store precision scores
    precision_log_0, precision_log_1 = [], []
    precision_rf_0, precision_rf_1 = [], []
    versions = list(l_y_test.keys())

    for key in versions:
        # Convert probabilities to binary predictions using the threshold
        y_pred_log_binary = [1 if prob >= threshold else 0 for prob in l_y_pred_log[key]]
        y_pred_rf_binary = [1 if prob >= threshold else 0 for prob in l_y_pred_rf[key]]

        # Compute precision scores for class 0 and class 1
        precision_log_0.append(precision_score(l_y_test[key], y_pred_log_binary, pos_label=0))
        precision_log_1.append(precision_score(l_y_test[key], y_pred_log_binary, pos_label=1))
        precision_rf_0.append(precision_score(l_y_test[key], y_pred_rf_binary, pos_label=0))
        precision_rf_1.append(precision_score(l_y_test[key], y_pred_rf_binary, pos_label=1))

    # Plot
    plt.figure(figsize=(12, 8))

    # Plot Precision for class 0
    plt.plot(versions, precision_log_0, label="Logistic Regression (Class 0)", marker='o', linestyle='-')
    plt.plot(versions, precision_rf_0, label="Random Forest (Class 0)", marker='s', linestyle='--')

    # Plot Precision for class 1
    plt.plot(versions, precision_log_1, label="Logistic Regression (Class 1)", marker='o', linestyle='-.')
    plt.plot(versions, precision_rf_1, label="Random Forest (Class 1)", marker='s', linestyle=':')

    # Add details to the plot
    plt.xlabel("Version")
    plt.ylabel("Precision Score")
    plt.title("Precision Score Evolution for Classes 0 and 1 by Version")
    plt.xticks(rotation=45)
    plt.grid(True)

    # Add the legend outside the plot
    plt.legend(
        title="Model and Class",
        bbox_to_anchor=(1.05, 1),  # Adjust this to control the position
        loc="upper left"
    )

    plt.tight_layout()

    # Display the plot
    plt.show()
