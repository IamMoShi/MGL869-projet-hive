from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE, RandomOverSampler  # Import SMOTE and RandomOverSampler
import pandas as pd
import os
from df_fusion import load_and_merge_csv
from sklearn.metrics import classification_report
import pandas as pd

def train_and_test_logistic_regression(directory, use_smote=True, use_random_over_sampler=False):
    """
    Load all CSV files from the given directory, merge them, and then train a logistic regression model
    on the resulting DataFrame using "Priority" as the target variable.

    Parameters:
        directory (str): The directory containing the CSV files.
        use_smote (bool): Whether to use SMOTE for oversampling the minority class.
        use_random_over_sampler (bool): Whether to use RandomOverSampler for oversampling the minority class.

    Returns:
        dict: A global classification report aggregating results from all folds.
    """
    # Load and merge CSV files
    merged_df = load_and_merge_csv(directory)

    # Display the count of representatives in each category
    category_counts = merged_df['Priority'].value_counts()
    print("Number of representatives in each category (Priority):")
    print(category_counts)

    # Drop the columns "BugStatus" and "BugCount"
    X = merged_df.drop(columns=['BugStatus', 'BugCount', 'Name', 'Priority'])

    # Encode the target variable "Priority" (nominal classification)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(merged_df['Priority'])

    # Initialize KFold and Logistic Regression model
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    logistic_model = LogisticRegression(solver='lbfgs', max_iter=500)

    # To store classification reports for each fold
    all_reports = []

    # Initialize the resampling technique
    if use_smote:
        resampler = SMOTE(random_state=42)
    elif use_random_over_sampler:
        resampler = RandomOverSampler(random_state=42)
    else:
        resampler = None

    # Perform K-Fold cross-validation
    for fold, (train_index, test_index) in enumerate(kf.split(X)):
        # Split into train and test sets
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Apply resampling technique (if specified)
        if resampler:
            X_train_res, y_train_res = resampler.fit_resample(X_train, y_train)
        else:
            X_train_res, y_train_res = X_train, y_train

        # Train the model on the resampled data
        logistic_model.fit(X_train_res, y_train_res)

        # Predict and generate classification report
        y_pred = logistic_model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

        # Append the report for the current fold
        all_reports.append(report)

    # Aggregate the reports (calculate the mean of precision, recall, f1-score for each category)
    global_report = {}
    categories = label_encoder.classes_

    # Initialize dictionaries to accumulate values
    precision_sum = {category: 0.0 for category in categories}
    recall_sum = {category: 0.0 for category in categories}
    f1_score_sum = {category: 0.0 for category in categories}
    support_sum = {category: 0 for category in categories}

    # Sum the metrics for each fold
    for report in all_reports:
        for category in categories:
            str_category = str(category)
            precision_sum[category] += report.get(str_category, {}).get('precision', 0.0)
            recall_sum[category] += report.get(str_category, {}).get('recall', 0.0)
            f1_score_sum[category] += report.get(str_category, {}).get('f1-score', 0.0)
            support_sum[category] += report.get(str_category, {}).get('support', 0)

    # Calculate the average values for each category
    num_folds = len(all_reports)
    for category in categories:
        global_report[category] = {
            'precision': precision_sum[category] / num_folds,
            'recall': recall_sum[category] / num_folds,
            'f1-score': f1_score_sum[category] / num_folds,
            'support': support_sum[category]
        }

    # Convert the global report to a DataFrame for better readability
    global_report_df = pd.DataFrame(global_report).T

    # Display the global report
    print("\nGlobal Classification Report (averaged over all folds):")
    print(global_report_df)

    return global_report_df


if __name__ == "__main__":
    # Train and test logistic regression model on the data using SMOTE
    print("Training with SMOTE...")
    classification_reports_smote = train_and_test_logistic_regression("data/full_metrics", use_smote=True)
    for key, report in classification_reports_smote.items():
        print(f"Classification report for {key}:")
        print(pd.DataFrame(report).transpose())
        print("\n")

    # Train and test logistic regression model on the data using RandomOverSampler
    print("Training with RandomOverSampler...")
    classification_reports_ros = train_and_test_logistic_regression("data/full_metrics", use_random_over_sampler=True)
    for key, report in classification_reports_ros.items():
        print(f"Classification report for {key}:")
        print(pd.DataFrame(report).transpose())
        print("\n")
