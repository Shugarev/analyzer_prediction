import os
import re
import pandas as pd
import numpy as np


def diff_list(li1, li2):
    return list(set(li1) - set(li2))

class DataHelper:
    # load the dataset
    def __init__(self, db_teach, db_test, col_factors, cat_features=[]):
        # store the inputs and outputs
        self.db_teach = db_teach
        self.db_test = db_test
        self.col_factors = sorted(col_factors)
        self.cat_features = cat_features
        self.num_features = diff_list(col_factors, cat_features)

        self.train = None
        self.test = None
        self.is_scaler = None
        self.scaler_params = None

    def create_train_test(self):
        col_factors = self.col_factors
        self.train = self.db_teach[col_factors].copy()
        self.test = self.db_test[col_factors].copy()

        self.train[self.num_features] = self.train[self.num_features].apply(pd.to_numeric, errors="coerce")
        self.test[self.num_features] = self.test[self.num_features].apply(pd.to_numeric, errors="coerce")

    def show_columns_with_na(self) -> (pd.Series, pd.Series):
        if self.train is None or self.test is None:
            print('incorrect train')
            print('incorrect test')
            return

        train_na_columns = self.train.columns[self.train.isnull().any(axis=0)]
        test_na_columns = self.test.columns[self.test.isnull().any(axis=0)]
        print("train na columns : {}" . format(train_na_columns))
        print("test na columns : {}" . format(test_na_columns))
        return train_na_columns, test_na_columns

    def get_mean_value(self) -> dict:
        mean_values = {}
        for col in self.num_features:
            value = self.train[col].mean()
            mean_values[col] = value
        return mean_values

    def replaced_na_values(self, replaced_values: dict):
        for col in self.num_features:
            replaced_val = replaced_values.get(col) or replaced_values.get('default')
            print(replaced_val)
            self.train[col] = self.train[col].fillna(replaced_val)
            self.test[col] = self.test[col].fillna(replaced_val)

    def get_scaler_params(self):
        if self.scaler_params is not None:
            print(' повторный вызов')
            return self.scaler_params
        self.scaler_params = {}
        for col in self.col_factors:
            x_min = self.train[col].min(axis=0)
            x_max = self.train[col].max(axis=0)
            self.scaler_params[col + "_min"] = x_min
            self.scaler_params[col + "_max"] = x_max
        return self.scaler_params

    def minMaxScaler_own(self):
        if self.is_scaler is not None:
            print(' повторный вызов')
            return

        if self.scaler_params is None:
            self.scaler_params = self.get_scaler_params()

        for col in self.col_factors:
            x_min = self.train[col].min()
            x_max = self.train[col].max()

            self.train[col] = (self.train[col] - x_min) / (x_max - x_min)
            self.test[col] = (self.test[col] - x_min) / (x_max - x_min)
            self.test[col] = np.where(self.test[col] > 1,  1, self.test[col])
            self.test[col] = np.where(self.test[col] < 0, 0, self.test[col])
        self.scaler_params = 1

    def add_status_in_train_test(self):
        self.train['status'] = self.db_teach.status.astype(np.int).copy()
        self.test['status'] = self.db_test.status.astype(np.int).copy()

    def get_numeric_features(self):
        return self.num_features

    def get_train_test(self):
        return self.train, self.test

def get_count_line(in_file):
    tmp_file = 'tmp-comand_info.txt'
    comand_line = 'wc -l ' + in_file + ' > ' + tmp_file
    os.system(comand_line)
    pattern = '[0-9]+'

    infile = open(tmp_file, 'r')
    firstLine = infile.readline()
    infile.close()
    os.remove(tmp_file)

    result = re.search(pattern, firstLine)
    count_line = result.group(0)
    return count_line

