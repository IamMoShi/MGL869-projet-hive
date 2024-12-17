import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from configparser import ConfigParser
from re import Pattern, compile
from os import path, cpu_count

import pandas as pd
from git import Repo, Commit


# Function to process a batch of commits
def process_commits(ids: set, commits: [Commit], repo_dir: str):
    # Load the repository in memory of the current thread
    local_repo: Repo = Repo(repo_dir)

    tuple_key_file_commit = []
    for commit_id in commits:
        for match in commits[commit_id]:
            hive_key = f'HIVE-{match}'
            if hive_key in ids:
                for file in local_repo.commit(commit_id).stats.files:
                    tuple_key_file_commit.append((hive_key, file, commit_id))
    return tuple_key_file_commit


def commit_analysis(ids: set) -> [(str, str, str)]:
    """
    Analyze the commits in the hive repository.
    Repository need to be cloned before calling this function.
    :return: List of tuples (issue, file, commit)
    """

    config = ConfigParser()
    config.read('config.ini')

    # Read the config file -------------------------------------------------- #

    hive_git_directory: str = config["GIT"]["HiveGitDirectory"]
    hive_git_repo_name: str = config["GIT"]["HiveGitRepoName"]
    commit_pattern: Pattern = compile(config["GIT"]["CommitPattern"])
    max_threads: int = int(config["GENERAL"]["MaxThreads"])
    data_directory: str = config["GENERAL"]["DataDirectory"]
    jira_csv_directory: str = config["JIRA"]["JiraCSVDirectory"]
    jira_tuple_directory: str = config["JIRA"]["JiraTuplesDirectory"]
    jira_tuples_csv: str = config["JIRA"]["JiraTuplesCSV"]
    query_each_run: str = config["JIRA"]["QueryEachRun"]
    query: str = config["JIRA"]["Query"]

    # Check if we need to download the Jira tuples -------------------------- #
    directory = path.join(data_directory, jira_csv_directory, jira_tuple_directory)
    command_file = path.join(directory, "command.txt")
    tuples_csv = path.join(directory, jira_tuples_csv)

    if not path.exists(directory):
        os.makedirs(directory)
    else:
        if path.exists(tuples_csv) and path.exists(command_file) and query_each_run != "Yes":
            with open(command_file, "r") as file:
                # Check if the command was the same last time :
                print("Checking if Jira tuples already created.")
                if file.read() == query:
                    print("Jira tuples already created.")
                    print(f"Data stored in '{tuples_csv}'")
                    df: pd.DataFrame = pd.read_csv(tuples_csv)
                    return list(df.itertuples(index=False, name=None))

    with open(command_file, "w") as file:
        file.write(query)

    # Variables ------------------------------------------------------------- #

    # Get the number of threads
    num_threads: int = min(max_threads, cpu_count())

    # List to store the couples (issue, file, commit)
    all_couples: [(str, str, str)] = []
    # Repo path
    repo_path: str = path.join(data_directory, hive_git_directory, hive_git_repo_name)
    # Load the repository
    repo: Repo = Repo(repo_path)
    # Split the commits into chunks
    chunk_size: int = len(list(repo.iter_commits())) // num_threads
    # Get all commits and files
    all_commits: [dict] = [{} for _ in range(num_threads)]

    # Prepare multi-threading chunks of commits -------------------------------- #

    for i, commit in enumerate(repo.iter_commits()):
        matches = commit_pattern.findall(commit.message)
        if matches:
            all_commits[i // chunk_size][commit.hexsha] = matches

    # Process the commits in parallel ------------------------------------------ #

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_commits, ids, chunk, repo_path) for chunk in all_commits]
        for future in as_completed(futures):
            couples = future.result()
            all_couples.extend(couples)

    with open(tuples_csv, "w") as file:
        df = pd.DataFrame(all_couples, columns=['issue', 'file', 'commit'])
        df.to_csv(file, index=False)

    print(f"{len(all_couples)} couples found.")
    print(f"Data stored in '{tuples_csv}'")

    return all_couples
