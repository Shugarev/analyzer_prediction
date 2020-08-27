import pandas as pd
import numpy as np
import random
from collections import Counter


class UtilsKy:
    # kyw3
    PATH_DATA_KYW3 = '/mnt/files/workdata/work/merchants/merchant_33_kyw3_2020-06-05/04_experiments/ex_01_some_teach/'
    DB_TEACH_KYW3 = PATH_DATA_KYW3 + 'db_teach_2_digit_status_kyw3_from_2019-11-20_to_2020-03-13.csv'
    DB_TEST_KYW3 = PATH_DATA_KYW3 + 'db_test_2_digit_status_kyw3a_from_2020-04-06_to_2020-05-06.csv'
    PATH_WHITE_KYW3 = '/mnt/files/workdata/work/merchants/merchant_33_kyw3_2020-06-05/08_white_lists/'
    WHITE_KYW3 = PATH_WHITE_KYW3 + 'white_list_kyw3_expeiment1_trusted_2020-02-20.csv'

    # ky9
    PATH_DATA_KY9 = '/mnt/files/workdata/work/merchants/merchant_32_ky9_2020-05-12_white_visa/04_experiments' \
                    '/ex_05_ky9_xgb_jupiter_2020_07_08/'
    DB_TEACH_KY9 = PATH_DATA_KY9 + 'db_teach_xgb_ky9.csv'
    DB_TEST_KY9 = PATH_DATA_KY9 + 'db_test_xgb_ky9.csv'
    DB_TEACH_KY9_ALL = '/mnt/files/workdata/work/merchants/merchant_32_ky9_2020-05-12_white_visa' \
                       '/04_experiments/ex_02_description/db_teach_700th_ky9_2018-12-19_2020-01-12.csv'

    DB_TEACH_KY9_300 = '/mnt/files/workdata/work/merchants/merchant_32_ky9_2020-05-12_white_visa/04_experiments' \
                       '/ex_02_description/db_teach_1m_ky9_2018-12-19_2020-01-12.csv'

    WHITE_KY9 = '/mnt/files/workdata/work/merchants/merchant_32_ky9_2020-05-12_white_visa/04_experiments' \
                '/white_lists/white_list_CardMasked_trusted_2019-12-17.csv'

    PATH_DATA_KY9_FOR_PROD = '/mnt/files/workdata/work/merchants/merchant_32_ky9_2020-05-12_white_visa/04_experiments' \
                             '/ex_06_for_prod/'
    DB_TEACH_KY9_FOR_PROD = PATH_DATA_KY9_FOR_PROD + 'db_teach_for_prod_ky9_2018-12-19_2020-04-02.csv'
    DB_TEST_KY9_FOR_PROD = PATH_DATA_KY9_FOR_PROD + 'db_test_for_prod_ky9_2020-04-02_2020-05-12.csv'

    GRAFANA_OPERATIONS = '/mnt/files/workdata/work/merchants/merchant_31_data_for_grafana/02_pure_data/' \
                         'operations_with_am_usd.csv'


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
        n_bad = dt_bad.shape[0]
        return round(100 * n_bad / n, 2)

    @classmethod
    def get_cb_rate_amount(cls, dt: pd.DataFrame) -> float:
        dt.amount = pd.to_numeric(dt.amount, errors="coerce")
        amount_dt = sum(dt.amount)
        amount_dt_bad = sum(dt_bad.amount)
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
        dt.amount = pd.to_numeric(dt.amount, errors="coerce")
        dt['amount_cb'] = np.where(cls.is_status_bad(dt), dt.amount, 0)
        dt_bad = cls.get_dt_bad(dt)
        dt_good = cls.get_dt_good(dt)

        mean_dt_bad = dt_bad.amount.mean()/20
        mean_dt_good = dt_good.amount.mean()/20

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

        stat_dt['true_amount_weight'] = (stat_dt.amount_bad + mean_dt_bad)/(all_bad_amount + mean_dt_bad)
        stat_dt['false_amount_weight'] = (stat_dt.amount_total - stat_dt.amount_bad + mean_dt_good)/(all_good_amount +
                                                                                                     mean_dt_good)
        stat_dt['true_weight'] = (stat_dt.n_bad + 1)/(all_bad + 1)
        stat_dt['false_weight'] = (stat_dt.n - stat_dt.n_bad + 1)/(all_good + 1)

        stat_dt['p'] = np.where(stat_dt.n_bad > 0, stat_dt.true_weight/(stat_dt.true_weight + stat_dt.false_weight), 0)
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
    def get_correlation_summarise_all_factors(cls, dt_1: pd.DataFrame, dt_2: pd.DataFrame) -> pd.DataFrame:
        result_df = pd.DataFrame(columns=['name', 'value'])
        col_list = dt_1.columns[dt_1.columns.isin(dt_2)]
        for col in col_list:
            st = Statistic.get_correlation_summarise(dt_1, dt_2, col)
            row = {"name": col, "value": st.iloc[0, 1]}
            result_df = result_df.append(row, ignore_index=True)
        return result_df

