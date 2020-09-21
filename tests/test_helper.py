import unittest
from tests.data_for_tests import DataForTests
from helper import get_count_line


class TestHelper(unittest.TestCase):

    def test_get_count_line(self):

        file_name = DataForTests.file_problem_lines
        result = get_count_line(file_name)
        expected = '8'
        self.assertEqual(result, expected, 'Count file in file is not correct')

