from matplotlib import pyplot as plt
from sklearn.metrics import roc_auc_score


def plot_AUC(y_test: dict, y_pred_log: dict, y_pred_rf: dict) -> None:
    versions = list(y_test.keys())

    # Logistic Regression
    auc_log = []
    for key in versions:
        auc_log.append(roc_auc_score(y_test[key], y_pred_log[key]))

    # Random Forest
    auc_rf = []
    for key in versions:
        auc_rf.append(roc_auc_score(y_test[key], y_pred_rf[key]))

    # Plot
    plt.figure(figsize=(10, 6))

    # Plot Logistic Regression
    plt.plot(
        versions, auc_log, label="Logistic Regression", marker='o', linestyle='-'
    )

    # Plot Random Forest
    plt.plot(
        versions, auc_rf, label="Random Forest", marker='s', linestyle='--'
    )

    # Add details to the plot
    plt.xlabel("Version")
    plt.ylabel("AUC Score")
    plt.title("AUC Score Evolution by Version")
    plt.xticks(rotation=45)
    plt.grid(True)
    # Add the legend outside the plot
    plt.legend(
        title="Model",
        bbox_to_anchor=(1.05, 1),  # Adjust this to control the position
        loc="upper left"
    )
    plt.tight_layout()

    # Display the plot
    plt.show()
