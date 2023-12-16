import argparse

from tree import parse_ignore_files_and_tree_included_only


def main():
    parser = argparse.ArgumentParser(
        description="Process files and display in a tree structure excluding specified patterns and directories.")
    parser.add_argument('-f', '--files', nargs='*', help='List of files to exclude', default=[])
    parser.add_argument('-d', '--dirs', nargs='*', help='List of directories to exclude', default=[])
    parser.add_argument('-g', '--gitignore', action='store_true', help='Use .gitignore files for exclusions')
    parser.add_argument('-k', '--dockerignore', action='store_true', help='Use .dockerignore files for exclusions')
    parser.add_argument('path', help='Directory path to process')
    parser.add_argument('--depth', type=int, help='Depth to traverse', default=None)

    args = parser.parse_args()

    parse_ignore_files_and_tree_included_only(
        user_excluded_files=args.files,
        user_excluded_dirs=args.dirs,
        gitignore=args.gitignore,
        dockerignore=args.dockerignore,
        path=args.path,
        depth=args.depth
    )


if __name__ == '__main__':
    main()
