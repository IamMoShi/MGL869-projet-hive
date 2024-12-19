from Objects import Version


def dev_count(version: Version) -> {str: int}:
    """
    Returns the number of developers that modified each file in the version.
    """
    ans: {str: int} = {}
    dev_memory: {str, set[str]} = {}
    commits: {"str": dict} = version.version_commits

    for commit_hash in commits:
        commit = commits[commit_hash]
        for file in commit["modified_files"]:
            file_name = file["filename"]
            if file_name not in ans:
                ans[file_name] = 0
                dev_memory[file_name] = set()
            if commit["email"] not in dev_memory[file_name]:
                dev_memory[file_name].add(commit["email"])
                ans[file_name] += 1
    return ans


def dev_count_r(version: Version) -> {str: int}:
    def recursive(v: Version, ans: {str: int}, dev_memory: {str, set[str]}):
        if v is None:
            return ans
        commits: {"str": dict} = v.version_commits

        for commit_hash in commits:
            commit = commits[commit_hash]
            for file in commit["modified_files"]:
                file_name = file["filename"]
                if file_name not in ans:
                    ans[file_name] = 0
                    dev_memory[file_name] = set()
                if commit["email"] not in dev_memory[file_name]:
                    dev_memory[file_name].add(commit["email"])
                    ans[file_name] += 1

        return recursive(v.getPreviousVersion(), ans, dev_memory)

    return recursive(version, {}, {})

def dev_exp(version: Version, ans: {str, int}) -> {str: int}:
    """

    Args:
        version: Studied version

    Returns: For each developer (email) until this version, the number of commits he made this version

    """
    commits: {"str": dict} = version.version_commits

    for commit_hash in commits:
        commit = commits[commit_hash]
        author = commit["email"]
        if author not in ans:
            ans[author] = 0
        ans[author] += 1

    return ans


def dev_exp_until(version: Version) -> {str: int}:
    ans: {str: int} = {}
    while version.getPreviousVersion() is not None:
        version = version.getPreviousVersion()
        ans = dev_exp(version, ans)
    return ans


def dev_mean_exp(version: Version) -> {str: int}:
    ans: {str: int} = {}
    dev_exp_dict = dev_exp_until(version)
    commits: {"str": dict} = version.version_commits

    for commit_hash in commits:
        commit = commits[commit_hash]
        author = commit["email"]
        for file in commit["modified_files"]:
            file_name = file["filename"]
            if file_name not in ans:
                ans[file_name] = []

            if author not in dev_exp_dict:
                ans[file_name] += [0]
            else:
                ans[file_name] += [dev_exp_dict[author]]

    for file in ans:
        if len(ans[file]) == 0:
            ans[file] = 0
        else:
            ans[file] = sum(ans[file]) / len(ans[file])

    return ans


def dev_min_exp(version: Version) -> {str: int}:
    ans: {str: int} = {}
    dev_exp_dict = dev_exp_until(version)
    commits: {"str": dict} = version.version_commits

    for commit_hash in commits:
        commit = commits[commit_hash]
        author = commit["email"]
        for file in commit["modified_files"]:
            file_name = file["filename"]

            if file_name not in ans:
                ans[file_name] = []

            if author not in dev_exp_dict:
                ans[file_name] += [0]
            else:
                ans[file_name] += [dev_exp_dict[author]]

    for file in ans:
        if len(ans[file]) == 0:
            ans[file] = 0
        else:
            ans[file] = min(ans[file])

    return ans