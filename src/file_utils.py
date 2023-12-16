import os


def get_files(path, depth=None, excluded_files=[], excluded_directories=[]):
    files = []
    # Normalize excluded directories to their absolute paths
    excluded_directories = [os.path.join(path, d) for d in excluded_directories]

    start_level = path.rstrip(os.sep).count(os.sep)
    for root, dirs, filenames in os.walk(path):
        # Calculate current level
        current_level = root.count(os.sep) - start_level

        # If depth is provided and current level exceeds it, stop going deeper
        if depth is not None and current_level >= depth:
            del dirs[:]

        # Include directories at the current level
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir_path not in excluded_directories:
                files.append(dir_path)
            else:
                # Remove excluded directories from the list of directories to traverse
                dirs.remove(dir)

        # Include files at the current level
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if filename not in excluded_files:
                files.append(file_path)

    return files


def parse_all_ignore_files_in_sub_directories(path, depth=None, gitignore=False, dockerignore=False):
    """
    Recursively parses all .gitignore and .dockerignore files in a given directory up to a specified depth.

    Args:
    - path (str): The path to the directory.
    - depth (int): The depth to traverse. 1 means only the given directory.
    - gitignore (str): Flag for exclusion of all contents of .gitignore files.
    - dockerignore (str): Flag for exclusion of all contents of .dockerignore files.

    Returns:
    - tuple: A tuple containing two lists: excluded_files and excluded_directories.
    """
    excluded_files = []
    excluded_directories = []

    for root, dirs, filenames in os.walk(path):
        # Check if current depth exceeds the specified depth
        if depth is not None and root[len(path):].count(os.sep) >= depth:
            del dirs[:]
            continue

        # Parse .gitignore and .dockerignore files
        if gitignore:
            gitignore_path = os.path.join(root, '.gitignore')
            gitignore_exclusions = get_gitignore_exclusions(gitignore_path)
            excluded_files.extend(gitignore_exclusions[0])
            excluded_directories.extend(gitignore_exclusions[1])

        if dockerignore:
            dockerignore_path = os.path.join(root, '.dockerignore')
            dockerignore_exclusions = get_dockerignore_exclusions(dockerignore_path)
            excluded_files.extend(dockerignore_exclusions[0])
            excluded_directories.extend(dockerignore_exclusions[1])

    return excluded_files, excluded_directories


def get_gitignore_exclusions(gitignore_path):
    return parse_ignore_file(gitignore_path)


def get_dockerignore_exclusions(dockerignore_path):
    return parse_ignore_file(dockerignore_path)


def parse_ignore_file(file_path):
    excluded_files = []
    excluded_directories = []

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                parse_line(line, excluded_directories, excluded_files)

    return excluded_files, excluded_directories


def parse_line(line, excluded_directories, excluded_files):
    line = line.strip()
    if line and not line.startswith("#"):
        if line.endswith('/'):
            excluded_directories.append(line[:-1])
        else:
            excluded_files.append(line)
