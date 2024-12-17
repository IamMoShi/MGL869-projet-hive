import git

from src.versions.tag_to_tuple import tag_to_tuple


def order_versions(versions: [git.Tag]) -> [git.Tag]:
    return sorted(versions, key=lambda x: tag_to_tuple(x))
