import os
import pandas as pd


def load_and_merge_csv(directory):
    """
    Load all CSV files from the given directory, merge them into a single DataFrame,
    and for rows with the same "Name", keep the row with the highest values for other columns.

    Parameters:
        directory (str): The directory containing the CSV files.

    Returns:
        pd.DataFrame: A merged DataFrame with the maximum values for each "Name".
    """
    # List to hold individual DataFrames
    df_list = []

    # Iterate over files in the directory
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path)
            df_list.append(df)

    # Merge all DataFrames into one
    merged_df = pd.concat(df_list, ignore_index=True)

    # Group by "Name" and get the row with the maximum values for each group
    merged_df = merged_df.groupby("Name", as_index=False).max()

    return merged_df


if __name__ == "__main__":
    # Load and merge CSV files from the "data/full_metrics" directory
    merged_df = load_and_merge_csv("data/full_metrics")
    print(merged_df)
    # Save the merged DataFrame to a CSV file
    merged_df.to_csv("data/full_merged_metrics.csv", index=False)
