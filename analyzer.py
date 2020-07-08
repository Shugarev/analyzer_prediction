import numpy as np
import pandas as pd


class HelperAnalyzer:

    BAD_STATUSES = (1, '1', 'true')

    def __init__(self, teach: pd.DataFrame, test: pd.DataFrame, white_list=None):

        bad_statuses = HelperAnalyzer.BAD_STATUSES
        self.N_WHITE_LIST = white_list.shape[0]

        self.N_TEACH = teach.shape[0]
        self.N_TEACH_BAD = teach[teach.status.isin(bad_statuses)].shape[0]

        self.N_TEST = test.shape[0]
        test.amount = pd.to_numeric(test.amount, errors="coerce")
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

    def __init__(self, teach: pd.DataFrame, test: pd.DataFrame, white_list=None):
        if white_list is None:
            white_list = self.get_empty_white_list()
        self.white_list = white_list
        self.teach = teach
        self.test = test
        self.params = HelperAnalyzer(teach, test, white_list)


    @classmethod
    def get_rating(cls, row: dict)->float:
        return float(row["p_1"]) + float(row["p_2"]) + float(row["p_3"]) + float(row["p_4"]) + float(row["p_5"])

    @classmethod
    def get_empty_white_list(cls)-> pd.DataFrame:
        return pd.DataFrame(columns=['ID'])

    @classmethod
    def get_empty_prediction_df(cls) -> pd.DataFrame:
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

    def get_count_3ds(self, percent: int)-> (float, float):
        test = self.get_convert_test()
        bad_statuses = HelperAnalyzer.BAD_STATUSES
        n_rows = round(self.params.N_TEST * percent / 100)
        test_first_n_rows = test.iloc[:n_rows, :]
        n_bad = test_first_n_rows[test_first_n_rows.status.isin(bad_statuses)].shape[0]
        result = str(round(100 * n_bad / self.params.N_TEST_BAD, 2))
        threshold = str(round(test.probability.values[n_rows - 1], 6))
        return float(result), float(threshold)

    def get_amount_3ds(self, percent: int)-> (float, float):
        test = self.get_convert_test()
        bad_statuses = HelperAnalyzer.BAD_STATUSES
        test_first_cumsum_rows = test[test.cum_amount < percent * self.params.AMOUNT_TEST / 100]
        amount_bad = sum(test_first_cumsum_rows[test_first_cumsum_rows.status.isin(bad_statuses)].amount)
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

    def get_convert_test(self)->pd.DataFrame:
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
