import unittest
import os
from tests.data_for_tests import DataForTests
from data_json.converter import Converter


class TestConverterJson(unittest.TestCase):

    def setUp(self):
        self.str_for_converter = DataForTests.str_for_converter
        self.converted_str = DataForTests.converted_str
        self.str_adds_quotes = DataForTests.str_adds_quotes
        self.input_file = DataForTests.intput_file
        self.output_file = DataForTests.output_file
        self.head_output_file = DataForTests.head_output_file
        self.json_load_for_patterns = DataForTests.json_load_for_patterns
        self.is_prb_line = DataForTests.is_prb_line
        self.json_load = DataForTests.json_load

    @classmethod
    def tearDownClass(cls):
        os.remove(DataForTests.output_file)

    def test_get_one_column_from_json(self):
        result = Converter.get_one_column_from_json(self.str_for_converter, "client.phone")
        expected = "923143****"
        self.assertEqual(result, expected, 'incorrect default data')

    def test_empty_get_one_column_from_json(self):
        result = Converter.get_one_column_from_json(self.str_for_converter, "notexist.col")
        expected = ''
        self.assertEqual(result, expected, 'incorrect default data')

    def test_get_flat_dictionary(self):
        result = Converter.get_flat_dictionary(self.converted_str)
        expected = {'client.phone': '923143****', 'client.name': 'Наталья Алтынбаева', 'client.email': 'aa49@mail.ru'}
        self.assertEqual(result, expected, 'incorrect default data')

    def test_update_json_by_pattern_1(self):
        line = r'{"email": "aaaaaaaa_aaaaaaa_2018@mail.ru\\n"}'
        result = Converter.update_json_by_pattern(line)
        expected = '{"email": "aaaaaaaa_aaaaaaa_2018@mail.ru"}'
        self.assertEqual(result, expected, r'incorrect update for pattern \\n ')

    def test_update_json_by_pattern_2(self):
        line = r'{"name":" ЧУП \\"Самелго-Плюс\\"     Сак"}'
        result = Converter.update_json_by_pattern(line)
        expected = '{"name":" ЧУП Самелго-Плюс     Сак"}'
        self.assertEqual(result, expected, r'incorrect update for pattern \\" ')

    def test_update_json_by_pattern_3(self):
        line = r'{"name":"ВАЛЕНТИНА\\\\ МЕНЧИКОВА"}'
        result = Converter.update_json_by_pattern(line)
        expected = '{"name":"ВАЛЕНТИНА  МЕНЧИКОВА"}'
        self.assertEqual(result, expected, r'incorrect update for pattern \\\\ ')

    def test_merge_flat_dictionary_keys_from_json_column(self):
        df = DataForTests.df_converter
        converter = Converter()
        result = converter.merge_flat_dictionary_keys_from_json_column(df, col_name='json')

        expected = ['client.phone', 'order.id', 'client.email']
        self.assertCountEqual(result, expected, r'incorrect update for pattern \\\\ ')

    def test_convert_one_column_from_json(self):
        df = DataForTests.df_converter
        col_json = 'json'
        col_name = 'client.email'
        result = Converter.convert_one_column_from_json(df, col_json, col_name)
        result = result.to_dict()
        expected = {0: 'aaaaaa49@mail.ru', 1: 'aaaa@gmail.com'}
        self.assertDictEqual(result, expected, 'incorrect default data')

    def test_convert_one_column_from_json_2(self):
        df = DataForTests.df_converter
        col_json = 'json'
        col_name = 'order.id'
        result = Converter.convert_one_column_from_json(df, col_json, col_name)
        result = result.to_dict()
        expected = {0: '', 1: '111111111'}
        self.assertDictEqual(result, expected, 'incorrect default data')

    def test_write_json_column_to_csv(self):
        df = DataForTests.df_converter
        col_name = "json"
        col_names = ['client.phone', 'client.email']
        converter = Converter()
        converter.write_json_column_to_csv(df, col_name, col_names, self.output_file)
        f = open(self.output_file, 'r')
        file_read = f.read()
        result = [file_read]
        expected = ['"client.phone","client.email"\n"923143****","aaaaaa49@mail.ru"\n"","aaaa@gmail.com"\n']
        self.assertEqual(result, expected, 'incorrect default data')

    def test_correct_json_load(self):
        result = Converter.correct_json_load(self.str_adds_quotes)
        print(result)
        expected = '{"is_trailer":"false","user_agent":"Mozilla/5.0 rv:52.0", "has_middle_name ":"true",' \
                   '"insurance_selected":"null"}'
        self.assertEqual(result, expected, 'incorrect default data')

    def test_write_json_column_to_csv_read_data_from_file(self):
        col_names = ["order.location", "client.email"]
        converter = Converter()
        converter.write_json_column_to_csv_read_data_from_file(self.input_file, col_names, self.output_file)
        f = open(self.output_file, 'r')
        file_read = f.read()
        result = [file_read]
        expected = ['"order.location","client.email"\n"","aaaaaaaa_aaaaaaa_2018@mail.ru"\n"ЧУП Самелго-Плюс Сак",'
                    '"aaaa@gmail.com"\n"",""\n']
        self.assertEqual(result, expected, 'incorrect default data')

    def test_get_default_csv_line(self):
        col_names = ["order.location", "client.email"]
        result = Converter.get_default_csv_line(col_names)
        expected = '"",""'
        self.assertEqual(result, expected, 'incorrect default data')

    def test_write_head_to_file(self):
        col_names = ["order.location", "client.email"]
        Converter.write_head_to_file(col_names, self.head_output_file)
        f = open(self.head_output_file, 'r')
        file_read = f.read()
        result = [file_read]
        expected = ['"order.location","client.email"\n']
        self.assertEqual(result, expected, 'incorrect default data')

    def test_update_json_by_pattern(self):
        result = Converter.update_json_by_pattern(self.json_load_for_patterns)
        expected = '{"is ":"false","user_agent":"Mo,zilla/5.0 rv:52.0"}'
        self.assertEqual(result, expected, 'incorrect default data')

    def test_is_problem_line(self):
        result = Converter.is_problem_line(self.is_prb_line)
        expected = 1
        self.assertEqual(result, expected, 'incorrect default data')

    def test_is_problem_line_2(self):
        result = Converter.is_problem_line(self.str_adds_quotes)
        expected = 0
        self.assertEqual(result, expected, 'incorrect default data')

    def test_get_csv_line_from_json(self):
        col_names = ["order.location", "client.email"]
        default_csv_line = ''
        converter = Converter()
        line_number = -1
        result = converter.get_csv_line_from_json(col_names, default_csv_line, self.json_load, line_number)
        expected = '"","aaaaaaaa_aaaaaaa_2018@mail.ru"'
        self.assertEqual(result, expected, 'incorrect default data')

    def test_get_csv_line_from_json_2(self):
        col_names = ["order.location", "client.phone", "client.email"]
        json_load = '{"client":{"phone": 923143, "email":"aaaaaaaa_aaaaaaa_2018@mail.ru"}}'
        default_csv_line = ''
        converter = Converter()
        line_number = -1
        result = converter.get_csv_line_from_json(col_names, default_csv_line, json_load, line_number)
        expected = '"","923143","aaaaaaaa_aaaaaaa_2018@mail.ru"'
        self.assertEqual(result, expected, 'incorrect default data')

    def test_not_extracted_json_col_by_regexp(self):
        converter = Converter()
        default_csv_line = ''
        line_number = -1
        line = 'NULL	Туту ЖД		NULL	2019-06-20 10:25:14'
        result = converter.not_extracted_json_col_by_regexp(default_csv_line, line, line_number)
        print(result)
        expected = ''
        self.assertEqual(result, expected, 'incorrect default data')

    def test_not_extracted_json_col_by_regexp_2(self):
        converter = Converter()
        default_csv_line = ''
        line_number = -1
        line = '2333 Туту ЖД {"order":{"id":"111111111"},"client":{"email":"aaaa@gmail.com"}} 2019-06-20 10:25:14'
        result = converter.not_extracted_json_col_by_regexp(default_csv_line, line, line_number)
        print(result)
        expected = ''
        self.assertEqual(result, expected, 'incorrect default data')
        pass
