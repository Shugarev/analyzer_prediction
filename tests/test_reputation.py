import unittest

from tests.data_for_tests import DataForTests
from reputation_factors.reputation import Reputation

message_sort = "df is not sort by id, problem column is {}"
message_factor = "Factor {} is not correct"

class TestReputation(unittest.TestCase):

    def setUp(self):
        self.df = DataForTests.df_rep

    def test_sort_data_check_id(self):
        reputation = Reputation(self.df)
        converted_df = reputation.df
        ids = converted_df.id.values
        ids = list(ids)
        expected = ['555444******0777_2022-09']*5 + ['666555******0666_2022-10']*4
        self.assertListEqual(ids, expected, message_sort.format('id'))

    def test_sort_data_check_date(self):
        reputation = Reputation(self.df)
        converted_df = reputation.df
        dates = converted_df.date.values
        dates = list(dates)
        expected = ['2020-01-01 17:12:11', '2020-01-10 15:50:20', '2020-01-20 10:01:05', '2020-03-10 12:10:10'
            ,'2020-04-10 12:14:15', '2019-01-01 12:20:12', '2020-05-10 14:11:01', '2020-05-10 15:12:03', '2020-05-10 15:32:05']
        self.assertListEqual(dates, expected, message_sort.format('date'))

    def test_sort_data_check_date_only(self):
        reputation = Reputation(self.df)
        converted_df = reputation.df
        date_only = converted_df.date_only.values
        date_only = list(date_only)
        expected = ['2020-01-01', '2020-01-10', '2020-01-20', '2020-03-10', '2020-04-10', '2019-01-01'
            ,'2020-05-10', '2020-05-10', '2020-05-10']
        self.assertListEqual(date_only, expected, message_sort.format('date_only'))

    def test_sort_data_check_status(self):
        reputation = Reputation(self.df)
        converted_df = reputation.df
        status = converted_df.status.values
        status = list(status)
        expected = [0, 0, 0, 1, 1, 0, 0, 1, 0]
        self.assertListEqual(status, expected, message_sort.format('status'))

    def test_sort_data_check_date_second(self):
        reputation = Reputation(self.df)
        converted_df = reputation.df
        date_second = converted_df.date_second.values
        date_second = list(date_second)
        expected = [1577898731, 1578671420, 1579514465, 1583842210, 1586520855,  1546345212, 1589119861
            ,1589123523, 1589124725]
        self.assertListEqual(date_second, expected, message_sort.format('date_second'))

    def test_sort_data_check_date_cb_second(self):
        # TOO test failed after rename field cb_second -> fa
        reputation = Reputation(self.df)
        converted_df = reputation.df
        date_cb_second = converted_df.cb_date_second.values
        date_cb_second = list(date_cb_second)

        expected = [-9223372037,-9223372037, -9223372037, 1585699200, 1588291200, -9223372037, -9223372037
            , 1590969600, -9223372037]
        self.assertListEqual(date_cb_second, expected, message_sort.format('date_cb_second'))

    def create_factors_by_id(self):
        pass

    def test_n_previous_factor(self):
        reputation = Reputation(self.df)
        df_factors = reputation.create_reputation_factors()
        n_previous = list(df_factors.n_previous.values)
        expected = [0, 0, 1, 2, 3, 4, 2, 1, 3]
        self.assertListEqual(n_previous, expected, message_factor.format('n_previous'))

    def test_n_grey_factor(self):
        reputation = Reputation(self.df)
        df_factors = reputation.create_reputation_factors()
        n_grey = list(df_factors.n_grey.values)
        expected = [0, 0, 0, 0, 3, 3, 1, 1, 1]
        self.assertListEqual(n_grey, expected, message_factor.format('n_grey'))

    def test_n_bad_factor(self):
        reputation = Reputation(self.df)
        df_factors = reputation.create_reputation_factors()
        n_bad = list(df_factors.n_bad.values)
        expected = [0, 0, 0, 0, 0, 1, 0, 0, 0]
        self.assertListEqual(n_bad, expected, message_factor.format('n_bad'))

    def test_is_quick_factor(self):
        reputation = Reputation(self.df)
        df_factors = reputation.create_reputation_factors()
        is_quick = list(df_factors.is_quick.values)
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 1]
        self.assertListEqual(is_quick, expected, message_factor.format('is-quick'))

    def test_is_first_factor(self):
        reputation = Reputation(self.df)
        df_factors = reputation.create_reputation_factors()
        is_first = list(df_factors.is_first.values)
        expected = [1, 1, 0, 0, 0, 0, 0, 0, 0]
        self.assertListEqual(is_first, expected, message_factor.format('is_first'))

    def test_n_in_day_factor(self):
        reputation = Reputation(self.df)
        df_factors = reputation.create_reputation_factors()
        n_in_day = list(df_factors.n_in_day.values)
        expected = [0, 0, 0, 0, 0, 0, 1, 0, 2]
        self.assertListEqual(n_in_day, expected, message_factor.format('n_in_day'))
