import unittest
import pandas as pd

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

    def test_stat_summarise_by_column_with_date(self):
        date_to_summarise = True
        result_df = self.statistic.get_stat_summarise_by_column(self.db_teach_with_date, 'bin', date_to_summarise)
        result_df = result_df.to_dict()
        self.assertDictEqual(result_df, DataForTests.EXPECTED_STAT_DT_WITH_DATE, 'incorrect default data')

    def test_train_test_split_with_diff_ids_size(self):
        df = DataForTests.df_split
        X_train, X_validation, y_train, y_validation = Statistic.train_test_split_with_diff_ids(df)

        self.assertEqual(X_train.shape[0], len(y_train), 'Xtrain, y_train have diff size')

        self.assertEqual(X_validation.shape[0], len(y_validation), 'X_validation, y_validation have diff size')

    def test_train_test_split_with_diff_ids_sample(self):
        df = DataForTests.df_split
        X_train, X_validation, y_train, y_validation = Statistic.train_test_split_with_diff_ids(df)

        X_train['status'] = y_train
        X_validation['status'] = y_validation

        X = pd.concat([X_train, X_validation])
        X.sort_values('n', inplace=True)

        df_dict = df.drop(columns=['id']).to_dict()
        X_dict = X.to_dict()

        self.assertDictEqual(df_dict, X_dict, 'Split is not full')

    def test_train_test_split_with_diff_ids_bad_id(self):
        df = DataForTests.df_split
        X_train, X_validation, y_train, y_validation = Statistic.train_test_split_with_diff_ids(df)

        X_train['status'] = y_train
        X_validation['status'] = y_validation

        df_train = pd.merge(X_train, df[['id', 'n']], how='left', on=['n'])
        df_validation = pd.merge(X_validation, df[['id', 'n']], how='left', on=['n'])

        mask = df_train.status.isin(Statistic.BAD_STATUSES)
        train_bad_ids = df_train[mask].id.unique()

        mask = df_validation.status.isin(Statistic.BAD_STATUSES)
        validate_bad_ids = df_validation[mask].id.unique()

        self.assertGreater(len(train_bad_ids), 0, 'X_train has no bad ids')
        self.assertGreater(len(validate_bad_ids), 0, 'X_validation has no bad ids')

        s_intersect = list(set(train_bad_ids) & set(validate_bad_ids))

        self.assertEqual(len(s_intersect), 0, 'X_train, X_validation have common bad ids. {}'.format(s_intersect))

    def test_train_test_split_with_diff_ids_good_id(self):
        df = DataForTests.df_split
        X_train, X_validation, y_train, y_validation = Statistic.train_test_split_with_diff_ids(df,
                                                                                                test_has_unique_ids=True)

        X_train['status'] = y_train
        X_validation['status'] = y_validation

        df_train = pd.merge(X_train, df[['id', 'n']], how='left', on=['n'])
        df_validation = pd.merge(X_validation, df[['id', 'n']], how='left', on=['n'])

        mask = df_train.status.isin(Statistic.BAD_STATUSES)
        train_good_ids = df_train[~mask].id.unique()

        mask = df_validation.status.isin(Statistic.BAD_STATUSES)
        validate_good_ids = df_validation[~mask].id.unique()

        self.assertGreater(len(train_good_ids), 0, 'X_train has no good ids')
        self.assertGreater(len(validate_good_ids), 0, 'X_validation has no good ids')

        s_intersect = list(set(train_good_ids) & set(validate_good_ids))

        self.assertEqual(len(s_intersect), 0, 'X_train, X_validation have common good ids.'.format(s_intersect))

    def test_get_quantile_stat(self):
        df = DataForTests.db_teach
        result = Statistic.get_quantile_stat(df, 'bin')
        expected_id = DataForTests.data_st
        result = result.to_dict()
        self.assertDictEqual(result, expected_id, 'incorrect default data')

