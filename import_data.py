from collections import Counter
import pandas as pd
import numpy as np
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.max_rows', 20)

import xgboost as xgb

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from statistic import Statistic
from utils import UtilsKy
from analyzer import HelperAnalyzer, AnalyzerPrediction

# for autoreload modules
%load_ext autoreload
%autoreload 2

# kyw3
path_data = '/mnt/files/workdata/work/merchants/merchant_33_kyw3_2020-06-05/04_experiments/ex_01_some_teach/'
db_teach = pd.read_csv(UtilsKy.DB_TEACH_KYW3, dtype=str, encoding='cp1251')
db_test = pd.read_csv(UtilsKy.DB_TEST_KYW3, dtype=str, encoding='cp1251')
white = pd.read_csv(UtilsKy.WHITE_KYW3 , dtype=str)