path_data = '/mnt/files/workdata/work/python-scripts/prediction_analyzer/predict_stock_quotes/data/'

file_old = path_data + '21K-predict.csv'
df_old = pd.read_csv(file_old,  dtype=str)

print(df_old.shape)
# (21129, 8)

file_new = path_data + 'data-2021-06-10/trainingset _1_.xlsx'
df_new = pd.read_excel(file_new, dtype=str)

print(df_new.shape)
# (29006, 6)

df_old_sub = df_old[['title', 'Unnamed: 2']].copy()
df_old_sub.columns = ['text', 'SENTIMENT']

df_new_sub = df_new[['title', 'znak']].copy()
df_new_sub.columns = ['text', 'SENTIMENT']

mask = df_new_sub['text'].isin(df_old_sub['text'])
df_unique =  df_new_sub[~ mask].copy()
print(df_unique.shape[0])

# df_new_sub - dataset c новыми данными

# df_old_sub - исходный dataset
# df_unique - dataset с отобранными новыми данными