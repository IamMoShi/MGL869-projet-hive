import os
import pydriller as pydriller
import git as git
import json

from configparser import ConfigParser


def extract_data(commit: pydriller.Commit) -> dict:
    commit_dict = {}
    commit_dict['hash'] = commit.hash
    commit_dict['author'] = commit.author.name
    commit_dict['email'] = commit.author.email
    commit_dict['author_date'] = commit.author_date.strftime("%Y-%m-%d %H:%M:%S")
    commit_dict['msg'] = commit.msg
    commit_dict['modified_files'] = []
    for modified_file in commit.modified_files:
        file = {}
        file['filename'] = modified_file.filename
        file['added_lines'] = modified_file.added_lines
        file['deleted_lines'] = modified_file.deleted_lines
        file['comments_changed'] = {'added': 0, 'deleted': 0}
        for n_line, line in modified_file.diff_parsed['added']:
            if "//" in line or "/*" in line:
                file['comments_changed']['added'] += 1
        for n_line, line in modified_file.diff_parsed['deleted']:
            if "//" in line or "/*" in line:
                file['comments_changed']['deleted'] += 1
        commit_dict['modified_files'].append(file)
    return commit_dict


def build_versions_commits(repo: git.Repo, filtered_versions: {str: str}) -> {str: dict}:
    """
    Build versions commits using Pydriller
    """
    config = ConfigParser()
    config.read("config.ini")

    skip_versions_build: bool = config["PYDRILLER"]["SkipVersionsBuild"].lower() == "yes"

    if skip_versions_build:
        print(f"Skipping full versions build")
        ans = {}
        if not os.path.exists(config["PYDRILLER"]["VersionsBuildDirectory"]):
            raise FileNotFoundError(f"Versions build directory not found")
        for key in filtered_versions:
            with open(os.path.join(config["GENERAL"]["VersionsBuildDirectory"], f"{key}.json"), "r") as f:
                ans[key] = json.load(f)
        return ans

    data_directory: str = config["GENERAL"]["DataDirectory"]
    versions_build_directory: str = config["PYDRILLER"]["VersionsBuildDirectory"]
    versions_build_path: str = os.path.join(data_directory, versions_build_directory)

    if not os.path.exists(versions_build_path):
        os.makedirs(versions_build_path)

    ans: {str: dict} = {}
    for key in filtered_versions:
        print(f"Building version {key}")
        pydriller_repo: pydriller.Repository = pydriller.Repository(repo.working_dir, to_tag=filtered_versions[key])
        ans[key] = {}
        for commit in pydriller_repo.traverse_commits():
            ans[key][commit.hash] = extract_data(commit)
        print(f"{len(ans[key])} commits extracted from version {key}")

        with open(os.path.join(versions_build_path, f"{key}.json"), "w") as f:
            json.dump(ans[key], f)

    return ans
