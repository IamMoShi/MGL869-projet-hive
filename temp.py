import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report

from configparser import ConfigParser
from src.IA_models import load_data

from sklearn.model_selection import KFold
import numpy as np

from sklearn.model_selection import KFold


def KFold_XY(n_splits, shuffle, random_state, X, y):
    """
    Perform K-Fold split on the dataset and return training and testing sets.

    Parameters:
        n_splits (int): Number of folds.
        shuffle (bool): Whether to shuffle the data before splitting.
        random_state (int): Random state for reproducibility.
        X (pandas.DataFrame): Features.
        y (pandas.Series or numpy.ndarray): Target labels.

    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    kf = KFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
    train_index, test_index = next(kf.split(X))  # Take the first split

    # Use iloc to properly index DataFrame rows
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    if isinstance(y, pd.Series):
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    else:  # Assume y is a numpy array
        y_train, y_test = y[train_index], y[test_index]

    return X_train, X_test, y_train, y_test


# Charger la configuration
config = ConfigParser()
config.read("config.ini")

DATA_DIRECTORY = config["GENERAL"]["DataDirectory"]
METRICS_DIRECTORY = "data/full_metrics"
N_SPLITS = int(config["IA"]["NSplits"])
SHUFFLE = config["IA"].getboolean("Shuffle")
RANDOM_STATE = int(config["IA"]["RandomState"])

# Charger les données
data_dict = load_data(METRICS_DIRECTORY)

# Préparer les données
XY_dict = {}
label_encoder = LabelEncoder()

for key in data_dict.keys():
    data: pd.DataFrame = data_dict[key]
    X = data.drop(columns=['BugStatus', 'Name', 'BugCount', 'Priority']).dropna(axis=1)  # Independent variables
    y_priority = data['Priority']  # Priority of the bug

    # Ensure y_priority is 1D
    if isinstance(y_priority, pd.Series):
        y_priority_encoded = label_encoder.fit_transform(y_priority)
    elif isinstance(y_priority, pd.DataFrame):
        y_priority_encoded = label_encoder.fit_transform(y_priority.squeeze())
    else:
        y_priority_encoded = label_encoder.fit_transform(np.array(y_priority))

    XY_dict[key] = (X, y_priority_encoded)

# Diviser les données avec K-Fold
XY_training_dict = {}
XY_testing_dict = {}

for key in XY_dict.keys():
    X, y = XY_dict[key]
    X_train, X_test, y_train, y_test = KFold_XY(N_SPLITS, SHUFFLE, RANDOM_STATE, X, y)
    XY_training_dict[key] = (X_train, y_train)
    XY_testing_dict[key] = (X_test, y_test)

# Entraîner le modèle et évaluer les résultats
results = []
# Assuming XY_training_dict and XY_testing_dict are already defined
logistic_regression_models = {}
classification_reports = {}

# Train logistic regression models
for key in XY_training_dict:
    X_train, y_train = XY_training_dict[key]
    log_model = LogisticRegression(solver='lbfgs', max_iter=500)
    log_model.fit(X_train, y_train)
    logistic_regression_models[key] = log_model

# Generate predictions and classification reports
for key in XY_testing_dict:
    X_test, y_test = XY_testing_dict[key]
    y_pred = logistic_regression_models[key].predict(X_test)
    report = classification_report(
        y_test, y_pred, output_dict=True, zero_division=0
    )
    classification_reports[key] = report

# Calculate precision and recall for each category and version
precision_by_category = {category: [] for category in range(len(label_encoder.classes_))}
recall_by_category = {category: [] for category in range(len(label_encoder.classes_))}

for key, report in classification_reports.items():
    for category in range(len(label_encoder.classes_)):
        str_category = str(category)
        precision_by_category[category].append(report.get(str_category, {}).get('precision', 0.0))
        recall_by_category[category].append(report.get(str_category, {}).get('recall', 0.0))

# Plot precision and recall for each category
import matplotlib.pyplot as plt

versions = list(XY_testing_dict.keys())

plt.figure(figsize=(15, 10))
for category in range(len(label_encoder.classes_)):
    plt.plot(
        versions, precision_by_category[category], label=f"Precision: Category {category}", marker='o'
    )
    plt.plot(
        versions, recall_by_category[category], label=f"Recall: Category {category}", linestyle='--'
    )

plt.xlabel("Version")
plt.ylabel("Score")
plt.title("Precision and Recall by Category and Version")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(
    title="Metrics", bbox_to_anchor=(1.05, 1), loc="upper left"
)
plt.tight_layout()
plt.show()

# Create a DataFrame for precision and recall
precision_df = pd.DataFrame(precision_by_category)
recall_df = pd.DataFrame(recall_by_category)

# Rename the columns to reflect the category names (optional)
precision_df.columns = [f"Category {category}" for category in precision_df.columns]
recall_df.columns = [f"Category {category}" for category in recall_df.columns]

# Combine precision and recall DataFrames
metrics_df = pd.concat([precision_df, recall_df], axis=1, keys=["Precision", "Recall"])

# Add the version names as row indices
metrics_df.index = versions

# Display the resulting DataFrame
print(metrics_df)

# Optionally, save the DataFrame to a CSV file
metrics_df.to_csv("precision_recall_by_category_and_version.csv")