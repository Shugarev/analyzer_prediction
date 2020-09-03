import unittest

from tests.data_for_tests import DataForTests
from statistic import Statistic


class TestStatistic(unittest.TestCase):
    def setUp(self):
        self.db_teach = DataForTests.db_teach
        self.db_teach_with_date = DataForTests.db_teach_with_date
        self.statistic = Statistic()

    def test_get_cb_rate(self):
        cb_rate = self.statistic.get_cb_rate(self.db_teach)
        expected_cb_rate = 40.0
        self.assertEqual(cb_rate, expected_cb_rate, 'incorrect data set')

    def test_get_cb_rate_amount(self):
        cb_rate_amount = self.statistic.get_cb_rate_amount(self.db_teach)
        expected_cb_rate_amount = 46.47
        self.assertEqual(cb_rate_amount, expected_cb_rate_amount, 'incorrect data set')

    def test_stat_summarise_by_column(self):
        result_df = self.statistic.get_stat_summarise_by_column(self.db_teach, 'bin')
        result_df_dict = result_df.to_dict()
        self.assertDictEqual(result_df_dict, DataForTests.EXPECTED_STAT_DT, 'incorrect default data')

    def test_stat_summarise_by_column_with_date(self, date_to_summarise=True):
        result_df = self.statistic.get_stat_summarise_by_column(self.db_teach_with_date, 'bin', date_to_summarise)
        result_df = result_df.to_dict()
        self.assertDictEqual(result_df, DataForTests.EXPECTED_STAT_DT_WITH_DATE, 'incorrect default data')
