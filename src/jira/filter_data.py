from configparser import ConfigParser
from os import path, listdir, makedirs, remove
import re

import pandas as pd


def fusion_affected_versions(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    This function fusions the affected versions of the data into a list of versions
    :param raw_data: The data that was downloaded from JIRA
    :return: A dataframe with the affected versions fused
    """
    affects_version_columns: [str] = [col for col in raw_data.columns if col.startswith('Affects Version/s')]
    raw_data['Affects Versions Combined'] = raw_data[affects_version_columns].apply(
        lambda x: ', '.join(x.dropna().astype(str)), axis=1
    )

    # Combine the versions into a single column
    fix_version_columns: [str] = [col for col in raw_data.columns if col.startswith('Fix Version/s')]

    raw_data['Fix Versions Combined'] = raw_data[fix_version_columns].apply(
        lambda x: ', '.join(x.dropna().astype(str)), axis=1
    )

    return raw_data


def keep_minor_and_major_version(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    !!! This function need to be run after the fusion_affected_versions function !!!
    This function keeps only the issue that have affected a minor or a major version of the software
    Major version are structured as X.0.0
    Minor version are structured as X.Y.0
    Everything else is considered as a patch or an alpha/beta version
    :param raw_data:
    :return: A dataframe with only the rows that have affected a minor or a major version
    """

    # Function to check if a version is a major or a minor version
    def is_major_or_minor(version: str) -> bool:
        if not isinstance(version, str):
            return False
        # Version majeure : X.0.0
        # Version mineure : X.Y.0
        return re.fullmatch(r'\d+\.0\.0', version) or re.fullmatch(r'\d+\.\d+\.0', version)

    # Filter the data
    filtered_data = raw_data[
        raw_data['Affects Versions Combined']
        .apply(lambda x: any(is_major_or_minor(v.strip()) for v in str(x).split(',')))
    ]

    return filtered_data


def keep_resolution_fixed(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    This function keeps only the rows that have the resolution fixed
    :param raw_data: The data that was downloaded from JIRA
    :return: A dataframe with only the rows that have the resolution fixed
    """
    return raw_data[raw_data['Resolution'] == 'Fixed']


def transform_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    This function transforms the data to keep only the columns that are needed for the analysis
    :param raw_data: The data that was downloaded from JIRA
    :return: A dataframe with the filtered columns
    """
    keep: [str] = ["Issue key", "Fix Versions Combined", "Affects Versions Combined", "Priority"]
    raw_data = fusion_affected_versions(raw_data)
    raw_data = keep_resolution_fixed(raw_data)
    raw_data = keep_minor_and_major_version(raw_data)
    return raw_data[keep]


def filter_data() -> pd.DataFrame:
    """
    This function keep only the columns that are needed for the analysis
    :return: A dataframe from the downloaded data
    """

    # Read the config file -------------------------------------------------- #

    config = ConfigParser()
    config.read('config.ini')
    section = 'JIRA'

    # Variables ------------------------------------------------------------- #

    base_url: str = config[section]["BaseUrl"]
    query: str = config[section]["Query"]
    jira_csv_directory: str = config[section]["JiraCSVDirectory"]
    query_each_run: str = config[section]["QueryEachRun"]
    jira_combined_csv: str = config[section]["JiraCombinedCSV"]
    jira_raw_csv_directory: str = config[section]["JiraRawCSVDirectory"]
    jira_filtered_csv_directory: str = config[section]["JiraFilteredCSVDirectory"]
    jira_filtered_csv: str = config[section]["JiraFilteredCSV"]

    data_directory: str = config["GENERAL"]["DataDirectory"]

    # The directory where the raw data are saved
    jira_raw_csv_path: str = path.join(data_directory, jira_csv_directory, jira_raw_csv_directory)

    combined_csv_path: str = path.join(jira_raw_csv_path, jira_combined_csv)

    # The directory where the filtered data will be saved
    jira_filtered_csv_path: str = path.join(data_directory, jira_csv_directory, jira_filtered_csv_directory)

    # File used to save the last command used to download the data
    command_file: str = path.join(jira_filtered_csv_path, "command.txt")

    # File that will be used for the analysis with filtered columns
    filtered_csv_path = path.join(jira_filtered_csv_path, jira_filtered_csv)

    if not path.exists(jira_raw_csv_path):
        raise FileNotFoundError(f"Raw data directory not found: {jira_raw_csv_path}")

    # Load the raw data
    raw_data = pd.read_csv(combined_csv_path, low_memory=False)

    if not path.exists(jira_filtered_csv_path):
        makedirs(jira_filtered_csv_path)
    else:
        csv_filtered_files = [f for f in listdir(jira_filtered_csv_path) if f.endswith(".csv")]

        # Check if the command in the command file is the same as the current query
        with open(command_file, 'r') as file:
            last_command = file.read()

        if last_command == query and csv_filtered_files and query_each_run != "Yes":
            print("Data already filtered")
            print(f"Data stored in '{filtered_csv_path}'")
            return pd.read_csv(filtered_csv_path, low_memory=False)

    # Delete the filtered file if it exists
    if path.exists(filtered_csv_path):
        remove(filtered_csv_path)

    with open(command_file, 'w') as file:
        file.write(query)

    # Filter the data
    raw_data = transform_data(raw_data)
    raw_data.to_csv(filtered_csv_path, index=False)
    print(f"Data stored in '{filtered_csv_path}'")
    return raw_data
