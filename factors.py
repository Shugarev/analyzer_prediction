import pandas as pd
import numpy as np
import re
from utils import Statistic


def is_only_digit(x:string)->int :
    x_char = re.sub('\\d', '', x)
    return 1 if x_char == '' else 0


def encode_length(x: str, encode: dict):
    if not x:
        return encode['unknown']
    len_x = str(len(x))
    return encode[len_x] if len_x in encode.keys() else encode['other']


def get_network(x):
    return re.sub('\\.\\d+$', '', x)


def get_local_net(x:str)->str:
    '''
    pattern = '(?<=\\.)\\d+$'
    result = re.search(pattern, x)
    result.group(0)
    '''
    return re.sub('^.+\\.', '', x)


class Factor:

    @classmethod
    def is_only_digit(cls, dt: pd.DataFrame,  col_name='zip')-> pd.Series:
        return dt[col_name].apply(lambda x: is_only_digit(x))

    @classmethod
    def encode_length(cls, dt: pd.DataFrame, col_name='phone', encode={'unknown': 0,'other': 0, '10': 1}) -> pd.Series:
        """
        Parameters
        ----------
        dt: pd.DataFrame
        FOR kyw3
        encode={'unknown': 0, - phone field is empty
                 'other': 0,  - all phone numbers different "10"
                 '10': 1      - for number has 10 characters
                 }

        Examples perl code
        --------
         hash_def => "m=>0, f=>0, other=>1, unknown=>1";
         hash_def => " unknown => 1, other => 0"
         keys other ,unknown are obligatory
         return
         $hash_encode{'unknown'} - if key does not exist or key is empty string
         $hash_encode{'other'}  - if key exists and key is not empty and $hash_encode{key} does not exist
         example hash_def => "m=>0,  unknown=>2, other=>3"
         $hash_encode{key} - if exists key and exists $hash_encode{key}
         """

        return dt[col_name].apply(lambda x: encode_length(x, encode))

    @classmethod
    def get_network(cls, dt: pd.DataFrame, col_name='ip') -> pd.Series:
        return dt[col_name].apply(lambda x: get_network(x))

    @classmethod
    def is_net_frequency(cls, teach: pd.DataFrame,  test: pd.DataFrame, threshold=10, col_name='ip'):
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
