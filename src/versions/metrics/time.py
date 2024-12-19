from datetime import datetime

from Objects import Version


def mean_time(version: Version) -> {str: float}:
    """
    Returns the mean time between each modification of each file in the version.
    """
    ans: {str: float} = {}
    time_memory: {str, list[datetime]} = {}
    commits: {"str": dict} = version.version_commits

    for commit_hash in commits:
        commit = commits[commit_hash]
        for file in commit["modified_files"]:
            file_name = file["filename"]
            if file_name not in ans:
                ans[file_name] = 0
                time_memory[file_name] = []
            time_memory[file_name].append(commit["author_date"])

    for file in time_memory:
        times = time_memory[file]
        if len(times) == 0 or len(times) == 1:
            ans[file] = 0
        else:
            ans[file] = sum(
                (times[i] - times[i - 1]).total_seconds() for i in range(1, len(times))
            ) / (len(times) - 1)

    return ans


def mean_time_r(version: Version) -> {str: float}:
    def recursive(v: Version, time_memory: {str, list[datetime]}):
        if v is None:
            return ans
        commits: {"str": dict} = version.version_commits

        for commit_hash in commits:
            commit = commits[commit_hash]
            for file in commit["modified_files"]:
                file_name = file["filename"]
                if file_name not in ans:
                    time_memory[file_name] = []
                time_memory[file_name].append(commit["author_date"])

        return recursive(v.getPreviousVersion(), time_memory)

    ans = {}
    time_memory = recursive(version, {})
    for file in time_memory:
        times = time_memory[file]
        if len(times) == 0 or len(times) == 1:
            ans[file] = 0
        else:
            ans[file] = sum(
                (times[i] - times[i - 1]).total_seconds() for i in range(1, len(times))
            ) / (len(times) - 1)
    return ans
