import numpy as np 
import pandas as pd 
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.max_rows', 20)

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import matthews_corrcoef

import os
for dirname, _, filenames in os.walk('df_tweets_wordcloud/'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        

import warnings
warnings.simplefilter('ignore')
%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from pprint import pprint
from datetime import datetime
import collections
import re

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from wordcloud import WordCloud
from collections import Counter        

# for autoreload modules
%load_ext autoreload
%autoreload 2