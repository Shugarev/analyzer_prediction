import os
import unittest
import pandas as pd

from read_csv_example.read_csv_helper import fixed_incorrect_html_field, fixed_incorrect_html_field_v2
from tests.data_for_tests import DataForTests


class TestIncorrectHtml(unittest.TestCase):
    def setUp(self):
        self.incorrect_html_file = DataForTests.incorrect_html_file
        self.correct_html_file = DataForTests.correct_html_file

    @classmethod
    def tearDownClass(cls):
         os.remove(DataForTests.correct_html_file)

    def test_fixed_incorrect_html(self):
        fixed_incorrect_html_field(self.incorrect_html_file, self.correct_html_file)
        df = pd.read_csv(self.correct_html_file, names=['amount', 'status', 'html'],  dtype=str, keep_default_na=False)
        d = df.to_dict()
        expected = {'amount': {0: '    "2391.19"', 1: '    "1734.02"'},
                    'status': {0: 'Success', 1: '500 proxy    Content-Type: text/html    Connection: close    <!DOCTYPE html PUBLIC -//W3C//DTD XHTML 1.1'},
                    'html': {0: 'authorize', 1: 'authorize'}}
        self.assertDictEqual(d, expected)

    def test_fixed_incorrect_html_v2(self):
        fixed_incorrect_html_field_v2(self.incorrect_html_file, self.correct_html_file)
        df = pd.read_csv(self.correct_html_file, names=['amount', 'status', 'html'], dtype=str, keep_default_na=False)
        d = df.to_dict()
        expected = {'amount': {0: '    "2391.19"', 1: '    "1734.02"'},
                    'status': {0: 'Success',
                               1: '500 proxy    Content-Type: text/html    Connection: close    <!DOCTYPE html PUBLIC -//W3C//DTD XHTML 1.1'},
                    'html': {0: 'authorize', 1: 'authorize'}}
        self.assertDictEqual(d, expected)
