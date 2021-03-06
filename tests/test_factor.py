import unittest

import pandas as pd
from factors import Factor
from factors import get_quantile
from tests.data_for_tests import DataForTests


class TestFactor(unittest.TestCase):
    def setUp(self):
        self.factor = Factor()
        self.db_teach_factor = DataForTests.db_teach_factor

    def test_get_is_zip_digit(self):
        result = self.factor.is_only_digit(self.db_teach_factor)
        result = result.tolist()
        self.assertListEqual(result, [1, 1, 0, 1, 0, 1, 0, 0, 1, 1], 'incorrect default data')

    def test_get_encode_length(self):
        result = self.factor.encode_length(self.db_teach_factor, encode={'unknown': 0,'other': 0, '10': 1})
        result = result.tolist()
        self.assertListEqual(result, [0, 1, 1, 0, 0, 0, 0, 0, 1, 0], 'incorrect default data')

    def test_get_encode_length_2(self):
        result = self.factor.encode_length(self.db_teach_factor, encode={'unknown': 3, 'other': 0, '10': 1})
        result = result.tolist()
        self.assertListEqual(result, [0, 1, 1, 0, 0, 3, 0, 0, 1, 0], 'incorrect default data')

    def test_get_encode_length_3(self):
        result = self.factor.encode_length(self.db_teach_factor, encode={'unknown': 3, 'other': 5, '10': 0})
        result = result.tolist()
        self.assertListEqual(result, [5, 0, 0, 5, 5, 3, 5, 5, 0, 5], 'incorrect default data')

    def test_get_network(self):
        result = self.factor.get_network(self.db_teach_factor)
        result = result.tolist()
        expected_ip = ['184.56.163', '204.210.126', '99.203.145', '69.181.49', '179.158.244', '166.137.175'
             ,'172.58.11', '174.202.7', '99.177.243', '73.108.11']
        self.assertListEqual(result, expected_ip, 'incorrect default data')

    def test_get_bin(self):
        result = self.factor.get_bin(self.db_teach_factor)
        result = result.tolist()
        expected_bin = ['547087','517148','546540','510805','544731','524038','551791','517805','517805','517805']
        self.assertListEqual(result, expected_bin, 'incorrect default data')

    def test_get_first_name(self):
        result = self.factor.get_first_name(self.db_teach_factor)
        result = result.tolist()
        expected_first_name = ['Gabriele', 'Malia', 'Stephen', 'Nicholas', 'Thiago', 'Jamal', 'Jorge', 'Joseph'
            , 'thomas', 'Micah']
        self.assertListEqual(result, expected_first_name, 'incorrect default data')

    def test_get_last_name(self):
        result = self.factor.get_last_name(self.db_teach_factor)
        result = result.tolist()
        expected_last_name = ['Markes', 'Gusman', 'Gordy', 'Saephanh', 'Fernandes', 'Stephens', 'Hernandez', 'Rusolo'
            , 'van', 'Pitchford']
        self.assertListEqual(result, expected_last_name, 'incorrect default data')

    def test_get_domain(self):
        result = self.factor.get_domain(self.db_teach_factor)
        result = result.tolist()
        expected_domain = ['markes.com', '4mail.com.net', '4roll.mail', 'gmail.com', 'pochta.net', 'yandex.com'
            , 'gmail.com', '4null.com.ua', 'hotmail.com', 'mail.ru']
        self.assertListEqual(result, expected_domain, 'incorrect default data')

    def test_get_last_domain_zone(self):
        result = self.factor.get_last_domain_zone(self.db_teach_factor)
        result = result.tolist()
        expected_last_dz = ['com', 'net', 'mail', 'com', 'net', 'com', 'com', 'ua', 'com', 'ru']
        self.assertListEqual(result, expected_last_dz, 'incorrect default data')

    def test_get_count_words_in_column(self):
        result = self.factor.get_count_words_in_column(self.db_teach_factor)
        result = result.tolist()
        self.assertListEqual(result, [3, 2, 3, 2, 2, 2, 5, 2, 3, 2], 'incorrect default data')

    def test_get_phone_2(self):
        result = self.factor.get_phone_2(self.db_teach_factor)
        result = result.tolist()
        expected_phone_2 = ['13', '10', '10', '11', '97', '', '71', '83', '10', '12']
        self.assertListEqual(result, expected_phone_2, 'incorrect default data')

    # @unittest.skip("demonstrating skipping")
    def test_get_phone_3(self):
        result = self.factor.get_phone_3(self.db_teach_factor)
        result = result.tolist()
        expected_phone_3 = ['135', '108', '100', '119', '977', '', '718', '832', '106', '128']
        self.assertListEqual(result, expected_phone_3, 'incorrect default data')

    def test_get_quantile(self):
        message = "incorrect interval for {}"
        q_amount = [0, 0.3, 0.8, 0.9]
        x = get_quantile(0.2, q_amount)
        self.assertEqual(x, 1, message.format(x))

        x = get_quantile(0.95, q_amount)
        self.assertEqual(x, 4, message.format(x))

    def test_set_amount_quantiles(self):
        message = "incorrect amount quantiles for {}"
        db_teach = pd.DataFrame({"amount": [100, 50, 80, 30, 20, 40, 50]})
        db_test = pd.DataFrame({"amount": [35, 20.5, 120, 0.2]})
        Factor.set_amount_quantiles(db_teach, db_test)
        self.assertListEqual(list(db_teach.amount_quntile.values), [6, 4, 5, 2, 1, 3, 4], message.format('teach'))
        self.assertListEqual(list(db_test.amount_quntile.values), [3, 1, 6, 1], message.format('test'))
