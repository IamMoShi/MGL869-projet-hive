import pandas as pd
from os import path, listdir, makedirs
from configparser import ConfigParser

# Configuration loaded once globally
config = ConfigParser()
config.read("config.ini")


def df_to_dict_version(filtered_bug_report_df: pd.DataFrame) -> dict:
    ans: dict = {}
    config = ConfigParser()
    config.read("config.ini")
    priority = config["GENERAL"]["BugPriorities"].replace(", ", ",").split(",")[::-1]

    for index, row in filtered_bug_report_df.iterrows():
        versions = row["Affects Versions Combined"].split(", ")
        for version in versions:
            version.strip()
            if version not in ans:
                ans[version] = []
            ans[version].append((row["Issue key"], priority.index(row["Priority"]) + 1))

    return ans


def df_to_dict_files(tuples_df: pd.DataFrame) -> dict:
    ans: dict = {}

    for index, row in tuples_df.iterrows():
        file = row["file"].split("/")[-1]
        if file not in ans:
            ans[file] = set()
        ans[file].add(row["issue"])
    return ans


def label_all_metrics() -> None:
    """
    Processes all metric files in the specified directory, labels files with BugStatus,
    and saves the results in the output directory.

    Parameters:
        couples_df (pd.DataFrame): DataFrame containing files with issues and their affected versions.
    """
    base_dir = config["GENERAL"]["DataDirectory"]
    metrics_directory = path.join(base_dir, config["OUTPUT"]["MetricsOutputDirectory"])
    output_dir = path.join(base_dir, config["OUTPUT"]["LabelledMetricsOutputDirectory"])
    csv_separator = config["GENERAL"].get("CSVSeparatorMetrics", ",")
    tuples_csv_path = path.join(base_dir, config["JIRA"]["JiraCSVDirectory"], config["JIRA"]["JiraTuplesDirectory"], config["JIRA"]["JiraTuplesCSV"])
    filtered_bug_report_path = path.join(base_dir, config["JIRA"]["JiraCSVDirectory"], config["JIRA"]["JiraFilteredCSVDirectory"], config["JIRA"]["JiraFilteredCSV"])

    if config['UNDERSTAND'].get('SkipLabellisation', 'No').lower() == 'yes':
        print("Labellisation process is skipped as per configuration.")
        return

    # Ensure the output directory exists
    if not path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        makedirs(output_dir)

    # # Extract only filenames from the 'File' column in the couples DataFrame
    # couples_df["Filename"] = couples_df["File"].apply(lambda x: path.basename(x))

    # Process all files in the metrics directory
    if not path.exists(metrics_directory):
        raise FileNotFoundError(f"Metrics directory not found: {metrics_directory}")

    if not path.exists(tuples_csv_path):
        raise FileNotFoundError(f"Tuples CSV file not found: {tuples_csv_path}")

    if not path.exists(filtered_bug_report_path):
        raise FileNotFoundError(f"Filtered bug report CSV file not found: {filtered_bug_report_path}")

    # Load tuples and filtered bug report
    tuples_df = pd.read_csv(tuples_csv_path, sep=csv_separator)
    tuples_dict = df_to_dict_files(tuples_df)

    filtered_bug_report_df = pd.read_csv(filtered_bug_report_path, sep=csv_separator)
    filtered_bug_report_dict = df_to_dict_version(filtered_bug_report_df)

    for metrics_file in listdir(metrics_directory):
        print(metrics_file)
        if metrics_file.endswith(".csv"):
            metrics_path = path.join(metrics_directory, metrics_file)
            print(f"Processing metrics file: {metrics_path}")
            try:
                # Load metrics
                metrics_df = pd.read_csv(metrics_path, sep=csv_separator, engine="python")
                if "Kind" not in metrics_df.columns:
                    raise KeyError(f"Column 'Kind' not found in {metrics_file}")

                # Filter rows where Kind == "File"
                metrics_df = metrics_df[metrics_df["Kind"] == "File"]
                metrics_df["BugStatus"] = 0
                metrics_df["BugCount"] = 0
                metrics_df["Priority"] = 0

                # Extract version from the file name
                version = metrics_file.replace("_metrics.csv", "")

                i = 0
                # Identify problematic files for the current version
                for index, row in metrics_df.iterrows():
                    file = row["Name"]
                    if file in tuples_dict:
                        for issue in tuples_dict[file]:
                            for couple in filtered_bug_report_dict.get(version):
                                if issue in couple[0]:
                                    metrics_df.loc[metrics_df["Name"] == file, "BugStatus"] = 1
                                    metrics_df.loc[metrics_df["Name"] == file, "BugCount"] += 1
                                    metrics_df.loc[metrics_df["Name"] == file, "Priority"] = couple[1]
                                    i += 1
                print(f"Number of bugs found in version {version}: {i}")

                # # Save labeled metrics to the output directory
                labeled_metrics_path = path.join(output_dir, f"{version}_labeled_metrics.csv")
                metrics_df.to_csv(labeled_metrics_path, index=False, sep=csv_separator)
                print(f"Labeled metrics saved to: {labeled_metrics_path}")
            except Exception as e:
                print(f"Error processing file {metrics_file}: {e}")
