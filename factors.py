import pandas as pd
import numpy as np
import re
from statistic import Statistic


def is_only_digit(x: str)->int:
    x_char = re.sub('\\d', '', x)
    return 1 if x_char == '' else 0


def encode_length(x: str, encode: dict):
    if not x:
        return encode['unknown']
    len_x = str(len(x))
    return encode[len_x] if len_x in encode.keys() else encode['other']


def encoded_map(x: str, encode: dict):
    if not x:
        return encode['unknown']
    return encode[x] if x in encode.keys() else encode['other']


def get_network(x):
    return re.sub('\\.\\d+$', '', x)


def get_local_net(x:str)->str:
    '''
    pattern = '(?<=\\.)\\d+$'
    result = re.search(pattern, x)
    result.group(0)
    '''
    return re.sub('^.+\\.', '', x)


def get_bin(x: str)->str:
    return x[:6]


def get_first_name(x: str)->str:
    x = re.sub("\\s+", " ", str(x))
    return x.split()[0]


def get_last_name(x: str)->str:
    x = re.sub("\\s+", " ", str(x))
    return x.split()[1]


def get_domain(x: str)->str:
    return str.split(x, '@')[1]


def get_last_domain_zone(x: str)->str:
    x = str.split(x, '@')[-1]
    return str.split(x, '.')[-1]


def get_count_words_in_column(x: str)->float:
    x = re.sub("[0-9*.,'-]", " ", str(x))
    x = re.sub("\\s+", " ", x)
    x = str.strip(x)
    return str.count(x, " ") + 1


def get_phone_2(x: str)->str:
    x = re.sub("\\D", "", str(x))
    return x[:2]


def get_phone_3(x: str)->str:
    x = re.sub("\\D", "", str(x))
    return x[:3]

def get_quantile(x, q_amount):
    n = len(q_amount)
    for i in range(1, n):
        if q_amount[i - 1] <= x < q_amount[i]:
            return i
    return n


class Factor:

    @classmethod
    def is_only_digit(cls, dt: pd.DataFrame, col_name='zip')-> pd.Series:
        return dt[col_name].apply(lambda x: is_only_digit(x))

    @classmethod
    def encode(cls, dt: pd.DataFrame, col_name='phone', encode={'unknown': 0, 'other': 0, '10': 1}) -> pd.Series:
        return dt[col_name].apply(lambda x: encoded_map(x, encode))

    @classmethod
    def encode_length(cls, dt: pd.DataFrame, col_name='phone', encode={'unknown': 0,'other': 0, '10': 1}) -> pd.Series:
        """
        Parameters
        ----------
        dt: pd.DataFrame (FOR kyw3)
        encode={'unknown': 0, - phone field is empty
                 'other': 0,  - all phone numbers different "10"
                 '10': 1      - for number has 10 characters
                 }
        """
        return dt[col_name].apply(lambda x: encode_length(x, encode))

    @classmethod
    def get_network(cls, dt: pd.DataFrame, col_name='ip') -> pd.Series:
        return dt[col_name].apply(lambda x: get_network(x))

    @classmethod
    def is_net_frequency(cls, teach: pd.DataFrame, test: pd.DataFrame, threshold=10, col_name='ip'):
        col_net = 'net'
        col_is = 'is_fr_net'
        teach[col_net] = cls.get_network(teach, col_name)
        test[col_net] = cls.get_network(test, col_name)

        s_network = Statistic.get_table_size(teach, col_net)
        net = list(s_network.index)
        net_n = list(s_network.values)
        dt = pd.DataFrame({col_net: net, 'count_net': net_n})
        dt_freq = dt[dt.count_net > threshold]
        net_frequency = dt_freq.network.unique()

        teach[col_is] = np.where(teach.network.isin(net_frequency), 1, 0)
        test[col_is] = np.where(test.network.isin(net_frequency), 1, 0)
        teach.drop(col_net,  axis=1)
        test.drop(col_net, axis=1)
        return teach.is_fr_net, test.is_fr_net

    @classmethod
    def get_bin(cls, dt: pd.DataFrame, col_name='card_masked') -> pd.Series:
        return dt[col_name].apply(lambda x: get_bin(x))

    @classmethod
    def get_first_name(cls, dt: pd.DataFrame, col_name='card_holder') -> pd.Series:
        return dt[col_name].apply(lambda x: get_first_name(x))

    @classmethod
    def get_last_name(cls, dt: pd.DataFrame, col_name='card_holder') -> pd.Series:
        return dt[col_name].apply(lambda x: get_last_name(x))

    @classmethod
    def get_domain(cls, dt: pd.DataFrame, col_name='email') -> pd.Series:
        return dt[col_name].apply(lambda x: get_domain(x))

    @classmethod
    def get_last_domain_zone(cls, dt: pd.DataFrame, col_name='email') -> pd.Series:
        return dt[col_name].apply(lambda x: get_last_domain_zone(x))

    @classmethod
    def get_count_words_in_column(cls, dt: pd.DataFrame, col_name='address') -> pd.Series:
        return dt[col_name].apply(lambda x: get_count_words_in_column(x))

    @classmethod
    def get_phone_2(cls, dt: pd.DataFrame, col_name='phone') -> pd.Series:
        return dt[col_name].apply(lambda x: get_phone_2(x))

    @classmethod
    def get_phone_3(cls, dt: pd.DataFrame, col_name='phone') -> pd.Series:
        return dt[col_name].apply(lambda x: get_phone_3(x))

    @classmethod
    def set_amount_quantiles(cls, db_teach: pd.DataFrame, db_test: pd.DataFrame,
                                                                            quantiles=[0.15, 0.25, 0.50, 0.75, 0.90]):
        db_teach.amount = pd.to_numeric(db_teach.amount, errors="coerce")
        db_test.amount = pd.to_numeric(db_test.amount, errors="coerce")
        amount_np = db_teach.amount.values
        q_amount = [np.quantile(amount_np, q) for q in quantiles]
        q_amount = [0] + q_amount
        db_teach['amount_quntile'] = db_teach.amount.apply(lambda x: get_quantile(x, q_amount))
        db_test['amount_quntile'] = db_test.amount.apply(lambda x: get_quantile(x, q_amount))
