import unittest
from pyfakefs.fake_filesystem_unittest import TestCase
from src.file_utils import get_files, parse_all_ignore_files_in_sub_directories


class TestFileUtils(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    # Tests for get_files
    def test_get_files_no_exclusions(self):
        self.fs.create_file('/test_dir/file1.txt')
        self.fs.create_file('/test_dir/file2.txt')
        self.fs.create_dir('/test_dir/subdir')
        self.fs.create_file('/test_dir/subdir/file3.txt')

        expected_files = ['/test_dir/file1.txt', '/test_dir/file2.txt', '/test_dir/subdir/file3.txt', '/test_dir/subdir']
        actual_files = get_files('/test_dir', depth=2)

        self.assertListEqual(sorted(actual_files), sorted(expected_files))

    def test_get_files_with_file_exclusions(self):
        self.fs.create_file('/test_dir/file1.txt')
        self.fs.create_file('/test_dir/file2.txt')

        expected_files = ['/test_dir/file2.txt']
        actual_files = get_files('/test_dir', depth=1, excluded_files=['file1.txt'])

        self.assertListEqual(sorted(actual_files), sorted(expected_files))

    def test_get_files_with_directory_exclusions(self):
        self.fs.create_file('/test_dir/file1.txt')
        self.fs.create_dir('/test_dir/excluded_dir')
        self.fs.create_file('/test_dir/excluded_dir/file2.txt')

        expected_files = ['/test_dir/file1.txt']
        actual_files = get_files('/test_dir', depth=2, excluded_directories=['excluded_dir'])

        self.assertListEqual(sorted(actual_files), sorted(expected_files))

    # Tests for parse_all_ignore_files_in_sub_directories
    def test_parse_no_ignore_files(self):
        self.fs.create_file('/test_dir/file1.txt')

        expected_result = ([], [])
        actual_result = parse_all_ignore_files_in_sub_directories('/test_dir', depth=1)

        self.assertEqual(actual_result, expected_result)

    def test_parse_with_gitignore(self):
        self.fs.create_file('/test_dir/.gitignore', contents='*.log\nexcluded_dir/')
        self.fs.create_file('/test_dir/file1.txt')
        self.fs.create_file('/test_dir/file2.log')
        self.fs.create_dir('/test_dir/excluded_dir')

        expected_result = (['*.log'], ['excluded_dir'])
        actual_result = parse_all_ignore_files_in_sub_directories('/test_dir', depth=1, gitignore=True)

        self.assertEqual(actual_result, expected_result)

    def test_parse_with_nested_dockerignore(self):
        self.fs.create_file('/test_dir/.dockerignore', contents='*.tmp')
        self.fs.create_file('/test_dir/subdir/.dockerignore', contents='*.cache')

        expected_result = (['*.tmp', '*.cache'], [])
        actual_result = parse_all_ignore_files_in_sub_directories('/test_dir', depth=2, dockerignore=True)

        self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
