from configparser import ConfigParser

import git
import re

from src.versions.tag_to_tuple import tag_to_tuple


def get_versions_tags(repo: git.Repo) -> [git.Tag]:
    all_tags: [git.Tag] = repo.tags
    ans: [git.Tag] = []

    config = ConfigParser()
    config.read('config.ini')  # TODO : change the path

    releases_regex = [re.compile(regex.strip()) for regex in config["GIT"]["ReleasesRegex"].split(",")]
    minimal_version: (int, int, int) = tuple(map(int, config["GENERAL"]["MinimalVersion"].split(".")))
    for tag in all_tags:
        if any(regex.match(tag.name) for regex in releases_regex):
            version = tag_to_tuple(tag)
            if version >= minimal_version:
                ans.append(tag)
    return ans


if __name__ == "__main__":
    # Need to adapt config.read path if used to test by running this file
    repo = git.Repo("../../data/hive_data/hiveRepo")
    get_versions_tags(repo)
