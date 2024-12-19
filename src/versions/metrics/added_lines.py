def added_lines(version: {str: dict}) -> {str: int}:
    """
    Returns the added lines of code for each file in the version.
    """
    ans: {str: int} = {}
    for commit_hash in version:
        for file in commit["modified_files"]:
            file_name = file["filename"]
            if file_name not in ans:
                ans[file_name] = 0
            ans[file_name] += file["added_lines"]
    return ans
