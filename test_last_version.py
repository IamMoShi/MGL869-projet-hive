import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder


def load_and_merge_csv(directory):
    """
    Load all CSV files from the given directory, merge them into one DataFrame.
    The CSV files are assumed to be sorted by version in the filename.

    Parameters:
        directory (str): The directory containing the CSV files.

    Returns:
        list: A list of DataFrames, one for each version.
    """
    files = sorted([f for f in os.listdir(directory) if f.endswith('.csv')], key=lambda x: x.split('_')[0])
    dataframes = []
    for file in files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        dataframes.append(df)
        if file == files[-1]:
            print(f"Last version is {file}")
    return dataframes


def train_and_test_on_versions(directory):
    """
    Train a logistic regression model on all versions except the last, and test it on the last version.

    Parameters:
        directory (str): The directory containing the versioned CSV files.

    Returns:
        dict: The classification report for the test set (last version).
    """
    # Step 1: Load and merge all CSV files from the directory
    dataframes = load_and_merge_csv(directory)

    # Ensure there are at least two files (versions) for training and testing
    if len(dataframes) < 2:
        raise ValueError("There should be at least two versions for training and testing.")

    # Step 2: Prepare the training set (all versions except the last)
    train_data = pd.concat(dataframes[:-1], ignore_index=True)  # Concatenate all but the last version
    test_data = dataframes[-1]  # The last version will be used for testing

    # Drop the columns "BugStatus", "BugCount", "Name" from the features
    X_train = train_data.drop(columns=['BugStatus', 'BugCount', 'Name', 'Priority'])
    y_train = train_data['Priority']
    X_test = test_data.drop(columns=['BugStatus', 'BugCount', 'Name', 'Priority'])
    y_test = test_data['Priority']

    # Encode the target variable "Priority" using LabelEncoder
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    # Step 3: Train the Logistic Regression model
    logistic_model = LogisticRegression(solver='lbfgs', max_iter=500_000_000)
    logistic_model.fit(X_train, y_train_encoded)

    # Step 4: Test the model on the last version and generate the classification report
    y_pred = logistic_model.predict(X_test)
    report = classification_report(y_test_encoded, y_pred, output_dict=True, zero_division=0)

    # Step 5: Display the classification report
    print("\nClassification Report (Tested on the last version):")
    print(pd.DataFrame(report).transpose())

    return report


if __name__ == "__main__":
    # Test the functions on the sample data
    directory = "data/full_metrics"
    train_and_test_on_versions(directory)