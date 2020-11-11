import numpy as np
import pandas as pd
from statistic import Statistic

class Encode:

    @classmethod
    def ordered_target_st(cls, db_teach: pd.DataFrame, db_test: pd.DataFrame,
                          col_name: str)->dict:
        message = 'column status on in {}'
        if 'status' not in list(db_teach):
            raise Exception(message.format('db_teach'))
        if 'status' not in list(db_test):
            raise Exception(message.format('db_test'))

        col_names = [col_name, 'status']
        df = db_teach[col_names].copy()
        df.status = np.where(df.status.isin(Statistic.BAD_STATUSES), 1, 0)

        g_df = df.groupby(col_name)
        df['n_bad_in_group'] = g_df['status'].apply(lambda g: g.cumsum())
        df['n_in_group'] = g_df.cumcount() + 1

        cb_rate = df.status.sum() / df.shape[0]
        a = 1
        df['encode'] = (df.n_bad_in_group - df.status + a * cb_rate) / (df.n_in_group + a)

        data = {'status': ['count', 'sum'], 'encode': 'mean'}

        dt = df.groupby(col_name).agg(data)
        dt.columns = ['n', 'n_bad', 'encode_group_mean']
        dt['encode_last'] = g_df.tail(1).encode.values
        dt['cb_rate'] = (dt.n_bad + a) / (dt.n + a)
        dt = dt.reset_index()

        db_test = db_test.copy()
        col_names = [col_name, 'cb_rate', 'encode_last', 'encode_group_mean']
        db_test = db_test.merge(dt[col_names], left_on=col_name, right_on=col_name, how='left')
        db_test.loc[:, 'cb_rate'].fillna(cb_rate, inplace=True)

        ret_val = {'encode_teach': df.encode.values,
                   'test_encode_group_mean': db_test.encode_group_mean.values,
                   'test_encode_last': db_test.encode_last.values,
                   'test_cb_rate': db_test.cb_rate.values
                   }
        return ret_val
