import os


def get_files(path, depth=1, excluded_files=[], excluded_directories=[]):
    """
    Recursively lists files in a given directory up to a specified depth.

    Args:
    - path (str): The path to the directory.
    - depth (int): The depth to traverse. 1 means only the given directory.
    - excluded_files (list): List of filenames to exclude.
    - excluded_directories (list): List of directory names to exclude.

    Returns:
    - list: A list of file paths.
    """
    files = []
    # Normalize excluded directories to their absolute paths
    excluded_directories = [os.path.join(path, d) for d in excluded_directories]

    for root, dirs, filenames in os.walk(path):
        # Check if current depth exceeds the specified depth
        if root[len(path):].count(os.sep) >= depth:
            del dirs[:]
            continue

        # Exclude specified directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in excluded_directories]

        # Add files to list, excluding the specified files
        for filename in filenames:
            if filename not in excluded_files:
                files.append(os.path.join(root, filename))

    return files


def parse_all_ignore_files_in_sub_directories(path, depth=1, gitignore=False, dockerignore=False):
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
        if root[len(path):].count(os.sep) >= depth:
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
    """
    Parses a .gitignore file and returns lists of excluded files and directories.

    Args:
    - gitignore_path (str): The path to the .gitignore file.

    Returns:
    - tuple: A tuple containing two lists: excluded_files and excluded_directories.
    """
    return parse_ignore_file(gitignore_path)


def get_dockerignore_exclusions(dockerignore_path):
    """
    Parses a .dockerignore file and returns lists of excluded files and directories.

    Args:
    - dockerignore_path (str): The path to the .dockerignore file.

    Returns:
    - tuple: A tuple containing two lists: excluded_files and excluded_directories.
    """
    return parse_ignore_file(dockerignore_path)


def parse_ignore_file(file_path):
    """
    Parses a .gitignore or .dockerignore file and returns lists of excluded files and directories.

    Args:
    - file_path (str): The path to the .gitignore or .dockerignore file.

    Returns:
    - tuple: A tuple containing two lists: excluded_files and excluded_directories.
    """
    excluded_files = []
    excluded_directories = []

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.endswith('/'):
                        excluded_directories.append(line[:-1])
                    else:
                        excluded_files.append(line)

    return excluded_files, excluded_directories
