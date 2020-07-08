import unittest
import pandas as pd

from analyzer import AnalyzerPrediction


d = {
    'id': ["427082******7013_2023-03", "414720******4963_2019-11", "434769******7655_2021-10"
    ,"434769******7655_2021-10", "407204******7425_2020-12", "483316******8724_2021-03", "483316******8724_2021-03"
    , "406032******1745_2021-07", "406032******1745_2021-07", "441103******6134_2021-07"]
    ,'status': [1, 0, 1, 1, 0, 0, 0, 0, 1, 0]
    , 'amount': ["264.75", "205.90", "22.24", "22.24", "42.36", "26.48", "31.77", "21.18", "21.18", "52.95"]
    }

db_teach = pd.DataFrame(data=d)

probability = [0.96, 0.83, 0.24, 0.37, 0.48, 0.74, 0.51, 0.21, 0.76, 0.61]

d['probability'] = probability

db_test = pd.DataFrame(data=d.copy())
db_test["probability"] = pd.to_numeric(db_test["probability"], errors="coerce")
db_test["amount"] = pd.to_numeric(db_test.amount, errors="coerce")

w = {"ID": ["414720******4963_2019-11",  "441103******6134_2021-07", "434769******7655_2021-10"]}

white = pd.DataFrame(data=w)

COL_NAMES = ['description', 'p_1', 'p_2', 'p_3', 'p_4', 'p_5', 'p_6', 'p_7', 'p_10', 'p_20', 'rating'
            , 'n_white_list', 'n_test_in_wl', 'n_test_bad_in_wl', 'amount_test_in_wl', 'amount_test_bad_in_wl'
            , 'n_teach', 'n_teach_bad', 'n_test', 'n_test_bad', 'amount_test_bad', 'amount_test']

ROW = {'amount_test': 711.04999999999995, 'amount_test_bad': 330.41000000000003
       , 'amount_test_bad_in_wl': 589.25999999999999, 'amount_test_in_wl': 303.33000000000004
       , 'description': 'Test1', 'n_teach': 10, 'n_teach_bad': 4, 'n_test': 10, 'n_test_bad': 4
       , 'n_test_bad_in_wl': 6, 'n_test_in_wl': 4, 'n_white_list': 3}

RESULT_DF = {'description': ["Test1", "threshold count"],'p_1': [0.0, 0.0],'p_2': [0.0, 0.0], 'p_3': [0.0, 0.0]
            , 'p_4': [0.0, 0.0], 'p_5': [0.0, 0.0], 'p_6': [25.00, 0.96], 'p_7': [25.00, 0.96]
            , 'p_10': [25.00, 0.96], 'p_20': [50.00, 0.76], 'rating': [15, 0.0], 'n_white_list': [3, 3]
            , 'n_test_in_wl': [4, 4], 'n_test_bad_in_wl': [6, 6], 'amount_test_in_wl': [303.33, 303.33]
            , 'amount_test_bad_in_wl': [589.26, 589.26], 'n_teach': [10, 10], 'n_teach_bad': [4, 4], 'n_test': [10, 10]
            , 'n_test_bad': [4, 4], 'amount_test_bad': [330.41, 330.41], 'amount_test': [711.05, 711.05]}


class WhiteTestCase(unittest.TestCase):

    def setUp(self):
        self.db_teach = db_teach
        self.db_test = db_test
        self.white = white
        self.anylyzer = AnalyzerPrediction(db_teach, db_test, white)
        self.anylyzer_without_wl = AnalyzerPrediction(db_teach, db_test)

    def test_get_rating(self):
        row = {"p_1": 1, "p_2": 2, "p_3": 3, "p_4": 4, "p_5": 5}
        result = self.anylyzer.get_rating(row)
        self.assertEqual(result, 15, 'incorrect rating')

    def test_get_empty_white_list(self):
        self.white = list(white['ID'])
        self.assertNotEqual(self.white, '', 'white list is empty')

    def test_get_empty_prediction_df_col_names(self):
        self.result_df = AnalyzerPrediction.get_empty_prediction_df()
        self.result_df = list(self.result_df)
        self.assertEqual(self.result_df, COL_NAMES, 'incorrect default columns')

    def test_get_xgb_weight(self):
        weight = [2, 1, 2, 2, 1, 1, 1, 1, 2, 1]
        result = self.anylyzer.get_xgb_weight()
        self.assertListEqual(list(result), weight, 'weight is incorrect')

    def test_get_count_3ds(self):
        percent = 20
        result, threshold = self.anylyzer.get_count_3ds(percent)
        self.assertEqual(result, 50.0, 'count is different')
        self.assertEqual(threshold, 0.76, 'threshold is different')

    def test_get_count_3ds_without_wl(self):
        percent = 20
        result, threshold = self.anylyzer_without_wl.get_count_3ds(percent)
        self.assertEqual(result, 25.0, 'count is different')
        self.assertEqual(threshold, 0.83, 'threshold is different')

    def test_get_amount_3ds(self):
        percent = 50
        result, threshold = self.anylyzer.get_amount_3ds(percent)
        self.assertEqual(result, 86.54, 'amount is different')
        self.assertEqual(threshold, 0.51, 'threshold is different')

    def test_get_amount_3ds_without_wl(self):
        percent = 50
        result, threshold = self.anylyzer_without_wl.get_amount_3ds(percent)
        self.assertEqual(result, 80.13, 'amount is different')
        self.assertEqual(threshold, 0.96, 'threshold is different')

    def test_get_row(self):
        description = "Test1"
        result_df = self.anylyzer.get_row(description)
        self.assertDictEqual(result_df, ROW, 'incorrect default columns or data')

    def test_get_convert_test(self):
        test = self.anylyzer.get_convert_test()
        self.assertCountEqual(test, db_test, 'incorrect data set')

    def test_get_table_prediction(self):
        description = "Test1"
        # result_df = self.anylyzer.get_table_prediction(description)
        # self.assertDictEqual(dict(result_df), RESULT_DF, 'incorrect default columns or data')




















