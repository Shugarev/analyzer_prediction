_positive = 'positive'
_negative = 'negative'
_neutral = 'neutral'

sentiment_list = [_neutral, _positive, _negative]
replaced_dic = {'0': _neutral, '1': _positive, '2': _negative}

#  ---df_old_sub
df_old_sub['sentiment'] = df_old_sub['SENTIMENT'].replace(replaced_dic)
print('df_old_sub.shape= ', df_old_sub.shape[0])

mask = df_old_sub.sentiment.isin(sentiment_list)
df_old_sub = df_old_sub[mask].copy()
print('df_old_sub.shape with correct sentiment= ', df_old_sub.shape[0])

#  ---df_new_sub
df_new_sub['sentiment'] = df_new_sub['SENTIMENT'].replace(replaced_dic)
print('df_new_sub.shape =', df_new_sub.shape[0])

mask = df_new_sub.sentiment.isin(sentiment_list)
df_new_sub = df_new_sub[mask].copy()
print('df_new_sub.shape =', df_new_sub.shape[0])

# ---create df_unique
mask = df_new_sub['text'].isin(df_old_sub['text'])
df_unique =  df_new_sub[~ mask].copy()

print('df_unique.shape with correct sentiment= ', df_unique.shape[0])

url_pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

def url(phrase):
    return url_pattern.sub('', phrase)

def prepare_data(dt: pd.DataFrame):
    mask = dt.text.notnull()
    dt = dt[mask].copy()

    dt['text'] = dt['text'].apply(url)

    dt.drop_duplicates(subset=['text'], keep='first', inplace=True)
    print(Counter(dt['sentiment']))
    
    return dt

# -- remove duplicate

print('df_old_sub.shape = ', df_old_sub.shape[0])
df_old_sub = prepare_data(df_old_sub)
print('df_old_sub.shape without duplicate = ', df_old_sub.shape[0])

print('df_unique.shape= ', df_unique.shape[0])
df_unique = prepare_data(df_unique)
print('df_unique.shape without duplicate = ', df_unique.shape[0])