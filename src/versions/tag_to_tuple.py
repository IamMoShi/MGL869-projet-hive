import git


def tag_to_tuple(tag: git.Tag) -> (int, int, int):
    return tuple(map(int, tag.name.split("-")[-1].split(".")))
