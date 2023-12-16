# Tree Script

## Purpose:
The Tree Script is a utility script that helps you process files and display them in a tree structure while excluding specified patterns and directories.
It also supports using `.gitignore` and `.dockerignore` files for exclusions.

## Usage:

### Linux (tree.sh):
Example usage on Linux:
```bash
bash tree.sh /path/to/directory -f file1 file2 -d dir1 dir2 -g -k --depth 3
```

### Windows (tree.bat):
Example usage on Windows:
```bash
tree.bat /path/to/directory -f file1 file2 -d dir1 dir2 -g -k --depth 3
```

## Flags:
<ul>
    <li>path: Directory path to process.</li>
    <li>-f, --files: List of files to exclude.</li>
    <li>-d, --dirs: List of directories to exclude.</li>
    <li>-g, --gitignore: Use `.gitignore` files for exclusions.</li>
    <li>-k, --dockerignore: Use `.dockerignore` files for exclusions.</li>
    <li>--depth: Depth to traverse (default is unlimited).</li>
</ul>
