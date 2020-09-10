import unittest
import os
from tests.data_for_tests import DataForTests
from data_json.converter import Converter
from data_json.converter import _get_one_column_from_json


class TestConverterJson(unittest.TestCase):

    def setUp(self):
        self.str_for_converter = DataForTests.str_for_converter
        self.converted_str = DataForTests.converted_str
        self.input_file = DataForTests.intput_file
        self.output_file = DataForTests.output_file

    @classmethod
    def tearDownClass(cls):
         os.remove(DataForTests.output_file)

    def test_get_one_column_from_json(self):
        result = _get_one_column_from_json(self.str_for_converter, "client.phone")
        expected = "923143****"
        self.assertEqual(result, expected, 'incorrect default data')

    def test_empty_get_one_column_from_json(self):
        result = _get_one_column_from_json(self.str_for_converter, "notexist.col")
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
        result = Converter.merge_flat_dictionary_keys_from_json_column(df, col_name='json')
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
        Converter.write_json_column_to_csv(df, col_name, col_names, self.output_file)
        f = open(self.output_file, 'r')
        file_read = f.read()
        result = [file_read]
        expected = ['"client.phone","client.email"\n"923143****","aaaaaa49@mail.ru"\n"","aaaa@gmail.com"\n']
        self.assertEqual(result, expected, 'incorrect default data')

    def test_write_json_column_to_csv_read_data_from_file(self):
        col_names = ["order.location", "client.email"]
        Converter.write_json_column_to_csv_read_data_from_file(self.input_file, col_names, self.output_file)
        f = open(self.output_file, 'r')
        file_read = f.read()
        result = [file_read]
        expected = ['"order.location","client.email"\n"","aaaaaaaa_aaaaaaa_2018@mail.ru"\n"ЧУП Самелго-Плюс Сак",'
                    '"aaaa@gmail.com"\n']
        self.assertEqual(result, expected, 'incorrect default data')

