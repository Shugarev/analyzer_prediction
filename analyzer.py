import numpy as np
import pandas as pd
from statistic import Statistic
from utils import Constant

class HelperAnalyzer:

    def __init__(self, teach: pd.DataFrame, test: pd.DataFrame, white_list=None):

        bad_statuses = Statistic.BAD_STATUSES
        self.N_WHITE_LIST = white_list.shape[0]

        self.N_TEACH = teach.shape[0]
        self.N_TEACH_BAD = Statistic.get_dt_bad(teach).shape[0]

        self.N_TEST = test.shape[0]
        test.amount = pd.to_numeric(test.amount, errors="coerce")
        self.AMOUNT_TEST = sum(test.amount)

        test["cum_amount"] = test.amount.cumsum()

        test_bad = Statistic.get_dt_bad(test)
        self.N_TEST_BAD = test_bad.shape[0]
        self.AMOUNT_TEST_BAD = sum(test_bad.amount)

        test_in_wl = test[test.id.isin(white_list.ID)]
        self.AMOUNT_TEST_IN_WL = sum(test_in_wl.amount)
        self.N_TEST_IN_WL = test_in_wl.shape[0]

        mask = (test.id.isin(white_list.ID)) & (test.status.isin(bad_statuses))
        test_bad_in_wl = test[mask]

        self.N_TEST_BAD_IN_WL = test_bad_in_wl.shape[0]
        self.AMOUNT_TEST_BAD_IN_WL = sum(test_bad_in_wl.amount)


class AnalyzerPrediction:

    def __init__(self, teach: pd.DataFrame, test: pd.DataFrame, white_list=None):
        if white_list is None:
            white_list = self.get_empty_white_list()
        self.white_list = white_list
        self.teach = teach
        self.test = test
        self.params = HelperAnalyzer(teach, test, white_list)

    @classmethod
    def get_rating(cls, row: dict):
        result = float(row["p_1"]) + float(row["p_2"]) + float(row["p_3"]) + \
                 float(row["p_4"]) + float(row["p_5"]) + float(row["p_6"]) + float(row["p_7"]) +\
                 float(row["p_10"]) + float(row["p_20"])
        return result

    @classmethod
    def get_empty_white_list(cls) -> pd.DataFrame:
        return pd.DataFrame(columns=['ID'])

    @classmethod
    def get_numbers_p_for_empty_prediction_df(cls, num_p: list or int) -> list:
        if type(num_p) == int:
            num_p = range(1, num_p + 1)
        p_cols = ['p_' + str(x) for x in num_p]
        return p_cols

    @classmethod
    def get_empty_prediction_df(cls, num_p=Constant.NUM_P) -> pd.DataFrame:
        description = ['description']
        main_cols = ['rating', 'n_white_list', 'n_test_in_wl', 'n_test_bad_in_wl', 'amount_test_in_wl',
                     'amount_test_bad_in_wl',
                     'n_teach', 'n_teach_bad', 'n_test', 'n_test_bad', 'amount_test_bad', 'amount_test']
        columns = description + num_p + main_cols

        result_df = pd.DataFrame(columns=columns)
        result_df.loc[:, description] = result_df.loc[:, description].astype(str)

        col_names = [col for col in result_df.columns if col.startswith('p_') or col.startswith('amount_')]
        col_names.append('rating')
        result_df.loc[:, col_names] = result_df.loc[:, col_names].astype(float)

        col_names = [col for col in result_df.columns if col.startswith('n_')]
        result_df.loc[:, col_names] = result_df.loc[:, col_names].astype(int)
        return result_df

    def get_xgb_weight(self) -> pd.Series:
        teach = self.teach
        n_sample = teach.shape[0]
        n_bad = Statistic.get_dt_bad(teach).shape[0]
        w = int(n_sample / n_bad)
        teach["amount"] = pd.to_numeric(teach.amount, errors="coerce")
        weight = np.where(Statistic.is_status_bad(teach), w, 1)
        return weight

    def get_count_3ds(self, percent: int)-> (float, float):
        test = self.get_convert_test()
        n_rows = round(self.params.N_TEST * percent / 100)
        test_first_n_rows = test.iloc[:n_rows, :]
        n_bad = Statistic.get_dt_bad(test_first_n_rows).shape[0]
        result = str(round(100 * n_bad / self.params.N_TEST_BAD, 2))
        threshold = str(round(test.probability.values[n_rows - 1], 6))
        return float(result), float(threshold)

    def get_amount_3ds(self, percent: int) -> (float, float):
        test = self.get_convert_test()
        test_first_cumsum_rows = test[test.cum_amount < percent * self.params.AMOUNT_TEST / 100]
        amount_bad = sum(Statistic.get_dt_bad(test_first_cumsum_rows).amount)
        result = str(round(100 * amount_bad / self.params.AMOUNT_TEST_BAD, 2))
        n_rows = test_first_cumsum_rows.shape[0]
        threshold = str(round(test.probability.values[n_rows - 1], 6))
        return float(result), float(threshold)

    def get_row(self, description: str)-> dict:
        params = self.params
        return {'description': description
            , 'n_teach': params.N_TEACH
            , 'n_teach_bad': params.N_TEACH_BAD
            , 'n_test': params.N_TEST
            , 'n_test_bad': params.N_TEST_BAD
            , 'amount_test_bad': params.AMOUNT_TEST_BAD
            , 'amount_test': params.AMOUNT_TEST
            , 'n_white_list': params.N_WHITE_LIST
            , 'n_test_in_wl': params.N_TEST_IN_WL
            , 'amount_test_in_wl': params.AMOUNT_TEST_IN_WL
            , 'n_test_bad_in_wl': params.N_TEST_BAD_IN_WL
            , 'amount_test_bad_in_wl': params.AMOUNT_TEST_BAD_IN_WL}

    def get_convert_test(self) -> pd.DataFrame:
        test = self.test.copy()
        white_list = self.white_list
        test["probability"] = pd.to_numeric(test["probability"], errors="coerce")
        test["amount"] = pd.to_numeric(test.amount, errors="coerce")
        test.loc[test.id.isin(white_list.ID), 'probability'] = 0
        test.sort_values(by="probability", ascending=False, inplace=True)
        test.cum_amount = test.amount.cumsum()
        return test

    def get_table_prediction(self, description='', result_df=np.nan, metric="count"):
        if type(result_df).__name__ != 'DataFrame':
            result_df = self.get_empty_prediction_df()

        row = self.get_row(description)
        row_threshold = row.copy()
        row_threshold['description'] = 'threshold ' + metric
        for col in result_df:
            if col.startswith('p_'):
                percent = int(col.split('_')[1])
                if metric == "amount":
                    row[col], row_threshold[col] = self.get_amount_3ds(percent)
                else:
                    row[col], row_threshold[col] = self.get_count_3ds(percent)

        row_threshold['rating'] = row['rating'] = self.get_rating(row)
        result_df = result_df.append([row, row_threshold], ignore_index=True)
        return result_df
