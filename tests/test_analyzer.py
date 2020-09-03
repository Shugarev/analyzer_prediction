import unittest

from analyzer import AnalyzerPrediction
from tests.data_for_tests import DataForTests


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.white = DataForTests.white
        self.analyzer = AnalyzerPrediction(DataForTests.db_teach, DataForTests.db_test, DataForTests.white)
        self.analyzer_without_wl = AnalyzerPrediction(DataForTests.db_teach, DataForTests.db_test)

    def test_get_rating(self):
        row = {"p_1": 1, "p_2": 2, "p_3": 3, "p_4": 4, "p_5": 5, "p_10": 10, "p_20": 20}
        result = self.analyzer.get_rating(row)
        self.assertEqual(result, 45, 'incorrect rating')

    def test_get_empty_white_list(self):
        white_list = list(self.white['ID'])
        self.assertNotEqual(white_list, '', 'white list is empty')

    def test_get_empty_prediction_df_col_names(self):
        result_df = AnalyzerPrediction.get_empty_prediction_df()
        result_df = list(result_df)
        self.assertEqual(result_df, DataForTests.COL_NAMES, 'incorrect default columns')

    def test_get_xgb_weight(self):
        expected_weight = [2, 1, 2, 2, 1, 1, 1, 1, 2, 1]
        result = self.analyzer.get_xgb_weight()
        self.assertListEqual(list(result), expected_weight, 'weight is incorrect')

    def test_get_count_3ds(self):
        percent = 20
        result, threshold = self.analyzer.get_count_3ds(percent)
        self.assertEqual(result, 50.0, 'count is different')
        self.assertEqual(threshold, 0.76, 'threshold is different')

    def test_get_count_3ds_without_wl(self):
        percent = 20
        result, threshold = self.analyzer_without_wl.get_count_3ds(percent)
        self.assertEqual(result, 25.0, 'count is different')
        self.assertEqual(threshold, 0.83, 'threshold is different')

    def test_get_amount_3ds(self):
        percent = 50
        result, threshold = self.analyzer.get_amount_3ds(percent)
        self.assertEqual(result, 86.54, 'amount is different')
        self.assertEqual(threshold, 0.51, 'threshold is different')

    def test_get_amount_3ds_without_wl(self):
        percent = 50
        result, threshold = self.analyzer_without_wl.get_amount_3ds(percent)
        self.assertEqual(result, 80.13, 'amount is different')
        self.assertEqual(threshold, 0.96, 'threshold is different')

    def test_get_row(self):
        description = "Test1"
        result_df = self.analyzer.get_row(description)
        self.assertDictEqual(result_df, DataForTests.EXPECTED_ROW, 'incorrect default columns or data')

    def test_get_convert_test(self):
        test = self.analyzer.get_convert_test()
        test = test.to_dict()
        self.assertDictEqual(test, DataForTests.DB_TEST, 'incorrect data set')

    def test_get_table_prediction(self):
        description = "Test1"
        result_df = self.analyzer.get_table_prediction(description)
        result_df = result_df.to_dict()
        self.assertDictEqual(result_df, DataForTests.EXPECTED_RESULT_DF, 'incorrect default columns or data')



