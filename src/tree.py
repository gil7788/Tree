import os

from file_utils import get_files, parse_ignore_file


def tree(files, root_path, depth):
    file_tree = {}
    root_parts = root_path.split(os.sep)

    for file in files:
        parts = file.split(os.sep)
        # Trim the parts of the path that are before the root_path
        parts = parts[len(root_parts):]

        # If the current level exceeds the desired depth, stop going deeper
        if depth is not None and len(parts) > depth:
            continue

        current_level = file_tree

        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

    return file_tree


def print_tree(current_tree, indent="", is_root=True):
    if is_root:
        print(".")
        indent = ""

    num_keys = len(current_tree)
    for i, (key, value) in enumerate(current_tree.items()):
        branch = "└── " if i == num_keys - 1 else "├── "
        print(indent + branch + key)

        if isinstance(value, dict):
            extension = "  " if i == num_keys - 1 else "│ "
            print_tree(value, indent + extension, is_root=False)


def parse_ignore_files_and_tree_included_only(user_excluded_files, user_excluded_dirs, gitignore,
                                              dockerignore, path, depth=None):
    # Parse the ignore files
    excluded_files = []
    excluded_directories = []
    if gitignore:
        gitignore_path = os.path.join(path, ".gitignore")
        excluded_files, excluded_directories = parse_ignore_file(gitignore_path)
    if dockerignore:
        # Read the .dockerignore files at different levels of your project
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                if filename == '.dockerignore':
                    dockerignore_file = os.path.join(root, filename)
                    dockerignore_exclusions = parse_ignore_file(dockerignore_file)
                    excluded_files.extend(dockerignore_exclusions[0])
                    excluded_directories.extend(dockerignore_exclusions[1])
    if user_excluded_files:
        excluded_files += user_excluded_files
    if user_excluded_dirs:
        excluded_directories += user_excluded_dirs

    files = get_files(path, depth, excluded_files, excluded_directories)
    files_tree = tree(files, path, depth)
    print_tree(files_tree)
