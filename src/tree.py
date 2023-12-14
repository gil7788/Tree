import os

from file_utils import get_files, get_gitignore_exclusions, get_dockerignore_exclusions, \
    parse_all_ignore_files_in_sub_directories


def tree(files, root_path):
    """
    Display the list of files in a tree structure, starting from the root_path.

    Args:
    - files (list): A list of file paths.
    - root_path (str): The root directory path from which the tree starts.

    Returns:
    - dict: A dictionary representing the tree structure.
    """
    file_tree = {}
    root_parts = root_path.split(os.sep)

    for file in files:
        parts = file.split(os.sep)
        # Trim the parts of the path that are before the root_path
        parts = parts[len(root_parts):]

        current_level = file_tree

        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

    return file_tree


def print_tree(current_tree, indent="", last=True, is_root=True):
    """
    Recursively prints a tree structure.

    Args:
    - current_tree (dict): A dictionary representing the tree structure.
    - indent (str): The indentation string used to represent tree levels.
    - last (bool): Flag to indicate if the current node is the last child in its level.
    - is_root (bool): Flag to indicate if the current node is the root of the tree.
    """
    if is_root:
        print(".")
        indent = ""

    num_keys = len(current_tree)
    for i, (key, value) in enumerate(current_tree.items()):
        branch = "└── " if i == num_keys - 1 else "├── "
        print(indent + branch + key)

        if isinstance(value, dict):
            extension = "    " if i == num_keys - 1 else "│   "
            print_tree(value, indent + extension, i == num_keys - 1, is_root=False)


def parse_ignore_files_and_tree_included_only(user_excluded_files, user_excluded_dirs, gitignore,
                                              dockerignore, path, depth=1):
    """
    Parses .gitignore and .dockerignore files and displays the list of included files in a tree structure.

    Args:
    - gitignore (str): Flag for exclusion of all contents of .gitignore files.
    - dockerignore (str): Flag for exclusion of all contents of .dockerignore files.
    - path (str): The path to the directory.
    - depth (int): The depth to traverse. 1 means only the given directory.

    Returns:
    - None: Prints the tree structure to the console.
    """
    excluded_ignore_files, excluded_ignore_directories = parse_all_ignore_files_in_sub_directories(path, depth, gitignore, dockerignore)
    excluded_files = user_excluded_files + excluded_ignore_files
    excluded_directories = user_excluded_dirs + excluded_ignore_directories
    files = get_files(path, depth, excluded_files, excluded_directories)
    files_tree = tree(files, path)
    print_tree(files_tree)
