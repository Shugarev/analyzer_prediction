import numpy as np
import pandas as pd


class HelperAnalyzer:

    BAD_STATUSES = (1, '1', 'true')

    def __init__(self, teach, test, white_list):
        bad_statuses = HelperAnalyzer.BAD_STATUSES

        self.N_WHITE_LIST = white_list.shape[0]

        self.N_TEACH = teach.shape[0]
        self.N_TEACH_BAD = teach[teach.status.isin(bad_statuses)].shape[0]

        self.N_TEST = test.shape[0]
        self.AMOUNT_TEST = sum(test.amount)
        test.cum_amount = test.amount.cumsum()

        test_bad = test[test.status.isin(bad_statuses)]
        self.N_TEST_BAD = test_bad.shape[0]
        self.AMOUNT_TEST_BAD = sum(test_bad.amount)

        test_in_wl = test[test.id.isin(white_list.ID)]
        self.AMOUNT_TEST_IN_WL = sum(test_in_wl.amount)
        self.N_TEST_IN_WL = test_in_wl.shape[0]

        mask = (test.id.isin(white_list.ID)) | (test.status.isin(bad_statuses))
        test_bad_in_wl = test[mask]

        self.N_TEST_BAD_IN_WL = test_bad_in_wl.shape[0]
        self.AMOUNT_TEST_BAD_IN_WL = sum(test_bad_in_wl.amount)


class AnalyzerPrediction:

    def __init__(self, teach, test, white_list):
        self.params = HelperAnalyzer(teach, test, white_list)
        self.teach = teach
        self.test = test
        self.white_list = white_list

    @classmethod
    def get_rating(row):
        return float(row["p_1"]) + float(row["p_2"]) + float(row["p_3"]) + float(row["p_4"]) + float(row["p_5"])

    @classmethod
    def get_empty_prediction_df(cls):
        result_df = pd.DataFrame(
            columns=['description', 'p_1', 'p_2', 'p_3', 'p_4', 'p_5'
                , 'p_6', 'p_7', 'p_10', 'p_20', 'rating'
                , 'n_white_list', 'n_test_in_wl', 'n_test_bad_in_wl'
                , 'amount_test_in_wl', 'amount_test_bad_in_wl'
                , 'n_teach', 'n_teach_bad'
                , 'n_test', 'n_test_bad', 'amount_test_bad', 'amount_test'
                    ])

        col_names = ['description']
        result_df.loc[:, col_names] = result_df.loc[:, col_names].astype(str)

        col_names = [col for col in result_df.columns if col.startswith('p_') or col.startswith('amount_')]
        col_names.append('rating')
        result_df.loc[:, col_names] = result_df.loc[:, col_names].astype(float)

        col_names = [col for col in result_df.columns if col.startswith('n_')]
        result_df.loc[:, col_names] = result_df.loc[:, col_names].astype(int)
        return result_df

    def get_xgb_weight(self) -> pd.Series:
        bad_statuses = HelperAnalyzer.BAD_STATUSES
        teach = self.teach
        n_sample = teach.shape[0]
        n_bad = teach[teach.status.isin(bad_statuses)].shape[0]
        w = int(n_sample / n_bad)
        teach["amount"] = pd.to_numeric(teach.amount, errors="coerce")
        weight = np.where(teach.status.isin(bad_statuses), w, 1)
        return weight

    def get_count_3ds(self, percent):
        test = self.test
        bad_statuses = HelperAnalyzer.BAD_STATUSES
        n_rows = round(self.params.N_TEST * percent / 100)
        test_first_n_rows = test.iloc[:n_rows, :]
        n_bad = test_first_n_rows[test_first_n_rows.status.isin(bad_statuses)].shape[0]
        result = str(round(100 * n_bad / self.params.N_TEST_BAD, 2))
        threshold = str(round(test.probability.values[n_rows - 1], 6))
        HelperAnalyzer.
        return result, threshold




