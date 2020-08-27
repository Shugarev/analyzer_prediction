import pandas as pd
import unittest

from factors import Factor


data = {'zip': ['56789', '96746', '45x01', '21540590', '1121D', '57075440', 'Rm4606', '020-72', '33015', '32514']
    , 'phone': ['1356789364528', '1086510074', '1002929855', '11994891341', '977852230', '', '7183741', '83292591'
        , '1065951413', '128298821232']
    , 'ip': ['184.56.163.85','204.210.126.255', '99.203.145.83', '69.181.49.246', '179.158.244.208', '166.137.175.69'
        , '172.58.11.54', '174.202.7.127', '99.177.243.220', '73.108.11.150']
    , 'card_masked': ['547087****8523', '517148****4111', '546540****4046', '510805****4554', '544731****8532'
        , '524038****4345', '551791****2736', '517805****4590', '517805****4126', '517805****4536']
    , 'card_holder': ['Gabriele Markes', 'Malia Gusman', 'Stephen Gordy', 'Nicholas Saephanh', 'Thiago Fernandes'
        , 'Jamal Stephens', 'Jorge Hernandez', 'Joseph Rusolo', 'thomas van', 'Micah Pitchford']
    , 'email': ['gabriele@markes.com', 'Fdaret1836@4mail.com.net', 'Vanwerd@4roll.mail', '18888_steven@gmail.com'
        , 'Hardcool12@pochta.net', 'StorestWin@yandex.com', '4334788@gmail.com', '585851@4null.com.ua'
        , 'AwertNord@hotmail.com', 'MerchAS@mail.ru']
    , 'address': ['Saint Brabus AMG 12', '5263 Ihilani place', '2111 Bishop Hill Road', '1502 International Blvd'
        , 'Rua sumidouro 35', '9 Highland St', '18336 NW 68th Ave Apt L', '6317 15th ave'
        , '9100 Baldridge road app 9324', '1204 Texas Avenue']
    }

db_teach = pd.DataFrame(data=data)


class TestFactor(unittest.TestCase):
    def setUp(self):
        self.factor = Factor()
        self.db_teach = db_teach

    def test_get_is_zip_digit(self):
        result = self.factor.is_only_digit(self.db_teach)
        result = result.to_list()
        self.assertListEqual(result, [1, 1, 0, 1, 0, 1, 0, 0, 1, 1], 'incorrect default data')

    def test_get_encode_length(self):
        result = self.factor.encode_length(self.db_teach, encode={'unknown': 0,'other': 0, '10': 1})
        result = result.to_list()
        self.assertListEqual(result, [0, 1, 1, 0, 0, 0, 0, 0, 1, 0], 'incorrect default data')

    def test_get_encode_length_2(self):
        result = self.factor.encode_length(self.db_teach, encode={'unknown': 3, 'other': 0, '10': 1})
        result = result.to_list()
        self.assertListEqual(result, [0, 1, 1, 0, 0, 3, 0, 0, 1, 0], 'incorrect default data')

    def test_get_encode_length_3(self):
        result = self.factor.encode_length(self.db_teach, encode={'unknown': 3, 'other': 5, '10': 0})
        result = result.to_list()
        self.assertListEqual(result, [5, 0, 0, 5, 5, 3, 5, 5, 0, 5], 'incorrect default data')

    def test_get_network(self):
        result = self.factor.get_network(self.db_teach)
        result = result.to_list()
        expected_ip = ['184.56.163', '204.210.126', '99.203.145', '69.181.49', '179.158.244', '166.137.175'
             ,'172.58.11', '174.202.7', '99.177.243', '73.108.11']
        self.assertListEqual(result, expected_ip, 'incorrect default data')

    def test_get_bin(self):
        result = self.factor.get_bin(self.db_teach)
        result = result.to_list()
        expected_bin = ['547087','517148','546540','510805','544731','524038','551791','517805','517805','517805']
        self.assertListEqual(result, expected_bin, 'incorrect default data')

    def test_get_first_name(self):
        result = self.factor.get_first_name(self.db_teach)
        result = result.to_list()
        expected_first_name = ['Gabriele', 'Malia', 'Stephen', 'Nicholas', 'Thiago', 'Jamal', 'Jorge', 'Joseph'
            , 'thomas', 'Micah']
        self.assertListEqual(result, expected_first_name, 'incorrect default data')

    def test_get_last_name(self):
        result = self.factor.get_last_name(self.db_teach)
        result = result.to_list()
        expected_last_name = ['Markes', 'Gusman', 'Gordy', 'Saephanh', 'Fernandes', 'Stephens', 'Hernandez', 'Rusolo'
            , 'van', 'Pitchford']
        self.assertListEqual(result, expected_last_name, 'incorrect default data')

    def test_get_domain(self):
        result = self.factor.get_domain(self.db_teach)
        result = result.to_list()
        expected_domain = ['markes.com', '4mail.com.net', '4roll.mail', 'gmail.com', 'pochta.net', 'yandex.com'
            , 'gmail.com', '4null.com.ua', 'hotmail.com', 'mail.ru']
        self.assertListEqual(result, expected_domain, 'incorrect default data')

    def test_get_last_domain_zone(self):
        result = self.factor.get_last_domain_zone(self.db_teach)
        result = result.to_list()
        expected_last_dz = ['com', 'net', 'mail', 'com', 'net', 'com', 'com', 'ua', 'com', 'ru']
        self.assertListEqual(result, expected_last_dz, 'incorrect default data')

    def test_get_count_words_in_column(self):
        result = self.factor.get_count_words_in_column(self.db_teach)
        result = result.to_list()
        self.assertListEqual(result, [3, 2, 3, 2, 2, 2, 5, 2, 3, 2], 'incorrect default data')

    def test_get_phone_2(self):
        result = self.factor.get_phone_2(self.db_teach)
        result = result.to_list()
        expected_phone_2 = ['13', '10', '10', '11', '97', '', '71', '83', '10', '12']
        self.assertListEqual(result, expected_phone_2, 'incorrect default data')

    def test_get_phone_3(self):
        result = self.factor.get_phone_3(self.db_teach)
        result = result.to_list()
        expected_phone_3 = ['135', '108', '100', '119', '977', '', '718', '832', '106', '128']
        self.assertListEqual(result, expected_phone_3, 'incorrect default data')
