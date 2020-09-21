import unittest

from find_problem_lines import show_problems_in_line, show_problem_lines_v2
from tests.data_for_tests import DataForTests


class TestFindProblemsLines(unittest.TestCase):
    def setUp(self):
        self.file_problem_lines = DataForTests.file_problem_lines

    def test_show_problems_in_line_1(self):
        line = ''
        result = show_problems_in_line(line)
        expected = 'The line is empty or contains only whitespace characters. The line has only backspace.'
        self.assertEqual(result, expected, 'incorrect default data')

    def test_show_problems_in_line_2(self):
        line = '464624","","chars"'
        result = show_problems_in_line(line)
        expected = 'The line does not starts with ". odd number of quotes in line. '
        self.assertEqual(result, expected, 'incorrect default data')

    def test_show_problems_in_line_3(self):
        line = '"464625","\n","\r"'
        result = show_problems_in_line(line)
        expected = 'The line has special symbol like \\n, \\r.'
        self.assertEqual(result, expected, 'incorrect default data')

    def test_show_problems_in_line_4(self):
        line = '"464626","\","\\"'
        result = show_problems_in_line(line)
        expected = 'The line has backslash.'
        self.assertEqual(result, expected, 'incorrect default data')

    def test_show_problems_in_line_5(self):
        line = '464627","chars","chars"'
        result = show_problems_in_line(line)
        expected = 'The line does not starts with ". odd number of quotes in line. '
        self.assertEqual(result, expected, 'incorrect default data')

    def test_show_problems_in_line_6(self):
        line = '"464627","chars","chars'
        result = show_problems_in_line(line)
        expected = 'The line does not ends with ". odd number of quotes in line. '
        self.assertEqual(result, expected, 'incorrect default data')

    def test_show_problems_in_line_7(self):
        line = '"464629","chars","ch"ars"'
        result = show_problems_in_line(line)
        expected = 'There are additional double quotes in the string. odd number of quotes in line. '
        self.assertEqual(result, expected, 'incorrect default data')

    def test_show_problem_lines_v2(self):
        problem_line = show_problem_lines_v2(self.file_problem_lines)
        result = problem_line.get_problem_data()
        expected = {'line': ['""', '"464625","\\n","\\r"', '"464626","\\","\\\\"', '464627","chars","chars"',
                    '"464628","chars,"chars', '"464629","chars","ch"ars"'], 'num': [2, 4, 5, 6, 7, 8],
                    'message': ['The line has only empty fields.', 'The line has backslash.',
                    'The line has backslash.', 'The line does not starts with ". odd number of quotes in line. ',
                    'The line does not ends with ".', 'There are additional double quotes in the string. '
                                                      'odd number of quotes in line. ']}
        self.assertCountEqual(result, expected, 'incorrect default data')
