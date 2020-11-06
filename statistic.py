import pandas as pd
import numpy as np
import random
from collections import Counter
from sklearn.model_selection import train_test_split


class Statistic:
    BAD_STATUSES = (1, '1', 'true')

    @classmethod
    def is_status_bad(cls, dt: pd.DataFrame) -> pd.Series:
        return dt.status.isin(Statistic.BAD_STATUSES)

    @classmethod
    def get_dt_good(cls, dt: pd.DataFrame) -> pd.DataFrame:
        return dt[~cls.is_status_bad(dt)]

    @classmethod
    def get_dt_bad(cls, dt: pd.DataFrame) -> pd.DataFrame:
        return dt[dt.status.isin(Statistic.BAD_STATUSES)]

    @classmethod
    def get_cb_rate(cls, dt: pd.DataFrame) -> float:
        n = dt.shape[0]
        dt_bad = cls.get_dt_bad(dt)
        n_bad = dt_bad.shape[0]
        return round(100 * n_bad / n, 2)

    @classmethod
    def get_cb_rate_amount(cls, dt: pd.DataFrame) -> float:
        dt_bad = cls.get_dt_bad(dt)
        amount_dt = sum(pd.to_numeric(dt.amount, errors="coerce"))
        amount_dt_bad = sum(pd.to_numeric(dt_bad.amount))
        result = round(100 * amount_dt_bad / amount_dt, 2)
        return result

    @classmethod
    def get_table(cls, dt: pd.DataFrame, col_name: str) -> Counter:
        return Counter(dt[col_name])

    @classmethod
    def get_table_value_counts(cls, dt: pd.DataFrame, col_name: str) -> pd.core.series.Series:
        return dt[col_name].value_counts()

    @classmethod
    def get_table_size(cls, dt: pd.DataFrame, col_name: str) -> pd.core.series.Series:
        return dt.groupby(col_name).size()

    @classmethod
    def get_table_agg(cls, dt: pd.DataFrame, col_name: str) -> pd.core.series.Series:
        dt_agg = dt.groupby(col_name).agg({col_name: "count"})
        dt_agg.columns = ['n_' + col_name]
        return dt_agg

    @classmethod
    def get_table_crosstab(cls, dt: pd.DataFrame, index_name: str, col_name: str) -> pd.core.frame.DataFrame:
        return pd.crosstab(index=dt[index_name], columns=dt[col_name], margins=True)  # с итогами

    @classmethod
    def get_stat_summarise_by_column(cls, dt: pd.DataFrame, col_name: str, date_to_summarise=False) -> pd.DataFrame:
        dt = dt.copy()
        dt.amount = pd.to_numeric(dt.amount, errors="coerce")
        dt['amount_cb'] = np.where(cls.is_status_bad(dt), dt.amount, 0)
        dt_bad = cls.get_dt_bad(dt)
        dt_good = cls.get_dt_good(dt)

        mean_dt_bad = dt_bad.amount.mean() / 20
        mean_dt_good = dt_good.amount.mean() / 20

        all_bad_amount = sum(dt_bad.amount)
        all_good_amount = sum(dt_good.amount)

        all_bad = dt_bad.shape[0]
        all_good = dt_good.shape[0]

        dt['is_status_bad'] = np.where(cls.is_status_bad(dt), 1, 0)

        data = {'amount': ['count', 'sum'], 'is_status_bad': 'sum', 'amount_cb': 'sum'}

        col_names_agg = ['n', 'amount_total', 'n_bad', 'amount_bad']

        if date_to_summarise:
            data['date'] = ['min', 'max']
            col_names_agg = col_names_agg + ['min', 'max']

        stat_dt = dt.groupby(col_name).agg(data)
        stat_dt.columns = col_names_agg
        stat_dt['cb_rate'] = round(100 * stat_dt.n_bad / stat_dt.n, 4)
        stat_dt['cb_rate_amount'] = round(100 * stat_dt.amount_bad / stat_dt.amount_total, 4)

        stat_dt['true_amount_weight'] = (stat_dt.amount_bad + mean_dt_bad) / (all_bad_amount + mean_dt_bad)
        stat_dt['false_amount_weight'] = (stat_dt.amount_total - stat_dt.amount_bad + mean_dt_good) / (all_good_amount +
                                                                                                       mean_dt_good)
        stat_dt['true_weight'] = (stat_dt.n_bad + 1) / (all_bad + 1)
        stat_dt['false_weight'] = (stat_dt.n - stat_dt.n_bad + 1) / (all_good + 1)

        stat_dt['p'] = np.where(stat_dt.n_bad > 0, stat_dt.true_weight / (stat_dt.true_weight + stat_dt.false_weight),
                                0)
        stat_dt['p_a'] = np.where(stat_dt.n_bad > 0, stat_dt.true_amount_weight / (stat_dt.true_amount_weight +
                                                                                   stat_dt.false_amount_weight), 0)
        return stat_dt

    @classmethod
    def add_random_list_column(cls, dt: pd.DataFrame, count_class=3) -> pd.Series:
        random.seed(123)
        n = dt.shape[0]
        return random.sample(list(range(1, count_class + 1)) * n, n)

    @classmethod
    def get_correlation_summarise(cls, dt_1: pd.DataFrame, dt_2: pd.DataFrame, factor_name: str
                                  , col_names=['p_x', 'p_y'], method='kendall') -> pd.DataFrame:
        st_1 = cls.get_stat_summarise_by_column(dt_1, factor_name)
        st_2 = cls.get_stat_summarise_by_column(dt_2, factor_name)
        all_st = pd.merge(st_1, st_2, how='left', on=[factor_name])
        return all_st[col_names].corr(method)

    @classmethod
    def get_correlation_summarise_all_factors(cls, dt_1: pd.DataFrame, dt_2: pd.DataFrame, method='kendall') \
            -> pd.DataFrame:
        '''
        :param method:
         Method of correlation:
            pearson : standard correlation coefficient
            kendall : Kendall Tau correlation coefficient
            spearman : Spearman rank correlation
        '''
        result_df = pd.DataFrame(columns=['name', 'value'])
        col_list = dt_1.columns[dt_1.columns.isin(dt_2)]
        for col in col_list:
            st = Statistic.get_correlation_summarise(dt_1, dt_2, factor_name=col, method=method)
            row = {"name": col, "value": st.iloc[0, 1]}
            result_df = result_df.append(row, ignore_index=True)
        return result_df

    @classmethod
    def train_test_split_with_diff_ids(cls, dt: pd.DataFrame, train_size=0.8, random_state=4321, test_has_unique_ids=False):
        '''
        Split dataframe into random train and test subsets.
        Train and test have no common bad ids.

        '''

        if 'id' not in list(dt):
            raise Exception("There is no id in dataframe.")

        df_good = Statistic.get_dt_good(dt).copy()
        df_bad = Statistic.get_dt_bad(dt).copy()

        bad_ids = df_bad.id.unique()
        trian_bad_id, test_bad_id = train_test_split(bad_ids, train_size=train_size, random_state=random_state)

        mask = df_bad.id.isin(trian_bad_id)
        X_train_bad = df_bad[mask].copy()

        mask = df_bad.id.isin(test_bad_id)
        X_test_bad = df_bad[mask].copy()

        if not test_has_unique_ids:
            X_train_good, X_test_good = train_test_split(df_good, train_size=train_size, random_state=random_state)
        else:
            good_ids = df_good.id.unique()
            trian_good_id, test_good_id = train_test_split(good_ids, train_size=train_size, random_state=random_state)

            mask = df_good.id.isin(trian_good_id)
            X_train_good = df_good[mask]

            mask = df_good.id.isin(test_good_id)
            X_test_good = df_good[mask]

        drop_column = ['id', 'status']

        X_train = pd.concat([X_train_bad, X_train_good])
        y_train = X_train.status
        X_train.drop(columns=drop_column, inplace=True)

        X_test = pd.concat([X_test_bad, X_test_good])
        y_test = X_test.status
        X_test.drop(columns=drop_column, inplace=True)

        return X_train, X_test, y_train, y_test

    @classmethod
    def get_quantile_stat(cls, dt: pd.DataFrame, col_name: str):
        dt = dt.copy()
        dt['is_status_bad'] = np.where(cls.is_status_bad(dt), 1, 0)

        data = {'amount': ['count', 'mean', 'std',
                           ('q1', lambda x: x.quantile(0.25)), 'median',
                           ('q3', lambda x: x.quantile(0.75))],
                            'is_status_bad': 'sum'}

        dt.amount = pd.to_numeric(dt.amount)
        dt = dt.groupby(col_name).agg(data)
        dt.columns = ['n', 'mean', 'std', 'q1', 'median', 'q3', 'n_bad']
        dt.sort_values(by='n', ascending=False, inplace=True)
        col_names = list(dt.columns)
        col_names = col_names[-1:] + col_names[:-1]
        return dt.loc[:, col_names]


