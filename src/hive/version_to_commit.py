from git import Repo, Commit, Tag


def version_to_commit(repository: Repo, version: (int, int, int)) -> Commit:
    """
    Get the commit tag for a specific version
    :param repository: Repository to get the commit from
    :param version: The version to get the commit for (Tag containing the version)
    :return: Commit - The commit for the version
    """
    tags: [Tag] = repository.tags
    version_str: str = ".".join(map(str, version))
    output = []
    for tag in tags:
        if version_str in tag.name:
            output.append(tag.commit)
    if len(output) == 0:
        raise ValueError(f"No commit found for version {version_str}")
    if len(output) > 1:
        raise ValueError(f"Multiple commits found for version {version_str}")

    return output[0]
