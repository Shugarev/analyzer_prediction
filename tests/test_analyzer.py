import pandas as pd
import unittest

from analyzer import AnalyzerPrediction
from utils import Statistic

w = {"ID": ["414720******4963_2019-11", "441103******6134_2021-07", "434769******7655_2021-10"]}
white = pd.DataFrame(data=w)

data = {'id': ["427082******7013_2023-03", "414720******4963_2019-11", "434769******7655_2021-10"
    , "434769******7655_2021-10", "407204******7425_2020-12", "483316******8724_2021-03", "483316******8724_2021-03"
    , "406032******1745_2021-07", "406032******1745_2021-07", "441103******6134_2021-07"]
    , 'status': [1, 0, 1, 1, 0, 0, 0, 0, 1, 0]
    , 'amount': ["264.75", "205.90", "22.24", "22.24", "42.36", "26.48", "31.77", "21.18", "21.18", "52.95"]
    , 'bin': ['510250', '510211', '510250', '510211', '510250', '510211', '510260', '510260', '510260', '510260']
    , 'probability': [0.96, 0.83, 0.24, 0.37, 0.48, 0.74, 0.51, 0.21, 0.76, 0.61]
        }

date = ['2019-11-20 09:39:36', '2019-11-21 10:39:36', '2019-11-27 03:49:36', '2019-11-29 19:39:36'
    , '2019-12-02 09:39:36', '2019-12-07 23:39:36', '2019-12-17 11:39:36', '2019-12-23 09:39:36'
    , '2019-12-24 08:39:36', '2019-12-25 14:39:36']

db_teach = pd.DataFrame(data=data)

db_teach_with_date = db_teach.copy()
db_teach_with_date['date'] = date

db_test = pd.DataFrame(data=data.copy())
db_test["probability"] = pd.to_numeric(db_test["probability"], errors="coerce")
db_test["amount"] = pd.to_numeric(db_test.amount, errors="coerce")

COL_NAMES = ['description', 'p_1', 'p_2', 'p_3', 'p_4', 'p_5', 'p_6', 'p_7', 'p_10', 'p_20', 'rating'
    , 'n_white_list', 'n_test_in_wl', 'n_test_bad_in_wl', 'amount_test_in_wl', 'amount_test_bad_in_wl'
    , 'n_teach', 'n_teach_bad', 'n_test', 'n_test_bad', 'amount_test_bad', 'amount_test']

EXPECTED_ROW = {'amount_test': 711.04999999999995, 'amount_test_bad': 330.41000000000003
    , 'amount_test_bad_in_wl': 589.25999999999999, 'amount_test_in_wl': 303.33000000000004
    , 'description': 'Test1', 'n_teach': 10, 'n_teach_bad': 4, 'n_test': 10, 'n_test_bad': 4
    , 'n_test_bad_in_wl': 6, 'n_test_in_wl': 4, 'n_white_list': 3}

DB_TEST = {'id': {0: '427082******7013_2023-03', 8: '406032******1745_2021-07', 5: '483316******8724_2021-03'
        , 6: '483316******8724_2021-03', 4: '407204******7425_2020-12', 7: '406032******1745_2021-07'
        , 1: '414720******4963_2019-11', 2: '434769******7655_2021-10', 3: '434769******7655_2021-10'
        , 9: '441103******6134_2021-07'}
    , 'status': {0: 1, 8: 1, 5: 0, 6: 0, 4: 0, 7: 0, 1: 0, 2: 1, 3: 1, 9: 0}
    , 'amount': {0: 264.75, 8: 21.18, 5: 26.48, 6: 31.77, 4: 42.36, 7: 21.18, 1: 205.9, 2: 22.24, 3: 22.24, 9: 52.95}
    , 'bin': {0: '510250', 8: '510260', 5: '510211', 6: '510260', 4: '510250', 7: '510260', 1: '510211'
        , 2: '510250', 3: '510211', 9: '510260'}
    , 'probability': {0: 0.96, 8: 0.76, 5: 0.74, 6: 0.51, 4: 0.48, 7: 0.21, 1: 0.0, 2: 0.0, 3: 0.0, 9: 0.0}
    , 'cum_amount': {0: 264.75, 8: 285.93, 5: 312.41, 6: 344.18, 4: 386.54, 7: 407.72, 1: 613.62, 2: 635.86
    , 3: 658.1, 9: 711.0500000000001}}

EXPECTED_RESULT_DF = {'description': {0: 'Test1', 1: 'threshold count'}, 'p_1': {0: 0.0, 1: 0.0}, 'p_2': {0: 0.0, 1: 0.0}
    , 'p_3': {0: 0.0, 1: 0.0}, 'p_4': {0: 0.0, 1: 0.0}, 'p_5': {0: 0.0, 1: 0.0}, 'p_6': {0: 25.0, 1: 0.96}
    , 'p_7': {0: 25.0, 1: 0.96}, 'p_10': {0: 25.0, 1: 0.96}, 'p_20': {0: 50.0, 1: 0.76}, 'rating': {0: 75.0, 1: 75.0}
    , 'n_white_list': {0: 3, 1: 3}, 'n_test_in_wl': {0: 4, 1: 4}, 'n_test_bad_in_wl': {0: 6, 1: 6}
    , 'amount_test_in_wl': {0: 303.33000000000004, 1: 303.33000000000004}
    , 'amount_test_bad_in_wl': {0: 589.26, 1: 589.26}, 'n_teach': {0: 10, 1: 10}, 'n_teach_bad': {0: 4, 1: 4}
    , 'n_test': {0: 10, 1: 10}, 'n_test_bad': {0: 4, 1: 4}, 'amount_test_bad': {0: 330.41, 1: 330.41}
    , 'amount_test': {0: 711.05, 1: 711.05}}

EXPECTED_STAT_DT = {'n': {'510211': 3, '510250': 3, '510260': 4}
    , 'amount_total': {'510211': 254.62, '510250': 329.35, '510260': 127.08}
    , 'n_bad': {'510211': 1, '510250': 2, '510260': 1}
    , 'amount_bad': {'510211': 22.24, '510250': 286.99, '510260': 21.18}
    , 'cb_rate': {'510211': 33.3333, '510250': 66.6667, '510260': 25.0}
    , 'cb_rate_amount': {'510211': 8.7346, '510250': 87.1383, '510260': 16.6667}
    , 'true_amount_weight': {'510211': 0.07882499894444649, '510250': 0.8702098888735693, '510260': 0.0756564702066755}
    , 'false_amount_weight': {'510211': 0.6137171323460444, '510250': 0.11863099642533326, '510260': 0.28418079684845704}
    , 'true_weight': {'510211': 0.4, '510250': 0.6, '510260': 0.4}
    , 'false_weight': {'510211': 0.42857142857142855, '510250': 0.2857142857142857, '510260': 0.5714285714285714}
    , 'p': {'510211': 0.48275862068965525, '510250': 0.6774193548387096, '510260': 0.411764705882353}
    , 'p_a': {'510211': 0.11381978854855095, '510250': 0.8800302473441175, '510260': 0.2102519031056441}}

EXPECTED_STAT_DT_WITH_DATE = EXPECTED_STAT_DT.copy()

min_date = {'510211': '2019-11-21 10:39:36', '510250': '2019-11-20 09:39:36', '510260': '2019-12-17 11:39:36'}
max_date = {'510211': '2019-12-07 23:39:36', '510250': '2019-12-02 09:39:36', '510260': '2019-12-25 14:39:36'}

EXPECTED_STAT_DT_WITH_DATE['min'] = min_date
EXPECTED_STAT_DT_WITH_DATE['max'] = max_date


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.db_teach = db_teach
        self.db_teach_with_date = db_teach_with_date
        self.db_test = db_test
        self.white = white
        self.analyzer = AnalyzerPrediction(db_teach, db_test, white)
        self.analyzer_without_wl = AnalyzerPrediction(db_teach, db_test)
        self.statistic = Statistic()

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
        self.assertEqual(result_df, COL_NAMES, 'incorrect default columns')

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
        self.assertDictEqual(result_df, EXPECTED_ROW, 'incorrect default columns or data')

    def test_get_convert_test(self):
        test = self.analyzer.get_convert_test()
        test = test.to_dict()
        self.assertDictEqual(test, DB_TEST, 'incorrect data set')

    def test_get_table_prediction(self):
        description = "Test1"
        result_df = self.analyzer.get_table_prediction(description)
        result_df = result_df.to_dict()
        self.assertDictEqual(result_df, EXPECTED_RESULT_DF, 'incorrect default columns or data')

    def test_stat_summarise_by_column(self):
        result_df = self.statistic.get_stat_summarise_by_column(db_teach, 'bin')
        result_df_dict = result_df.to_dict()
        self.assertDictEqual(result_df_dict, EXPECTED_STAT_DT, 'incorrect default data')

    def test_stat_summarise_by_column_with_date(self, date_to_summarise=True):
        result_df = self.statistic.get_stat_summarise_by_column(db_teach_with_date, 'bin', date_to_summarise)
        result_df = result_df.to_dict()
        self.assertDictEqual(result_df, EXPECTED_STAT_DT_WITH_DATE, 'incorrect default data')
