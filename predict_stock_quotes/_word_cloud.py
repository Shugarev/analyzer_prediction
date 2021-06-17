ticker_pattern = re.compile(r'(^\$[A-Z]+|^\$ES_F)')
ht_pattern = re.compile(r'#\w+')

ticker_dic = collections.defaultdict(int)
ht_dic = collections.defaultdict(int)

for text in df['text']:
    for word in text.split():
        if ticker_pattern.fullmatch(word) is not None:
            ticker_dic[word[1:]] += 1
        
        word = word.lower()
        if ht_pattern.fullmatch(word) is not None:
            ht_dic[word] += 1
            
            
word_dic =  collections.defaultdict(int)
for text in df['text']:
    for word in text.split():
        word_dic[word] += 1

word_df = pd.DataFrame.from_dict(word_dic, orient='index').rename(columns={0:'count'}).sort_values('count', ascending=False) 

q = word_df['count'].quantile(0.75)
mask = word_df['count'] >= q

COUNT_WORDS_DEFAULT = word_df[mask].shape[0]
COUNT_WORDS_DEFAULT = 1000


# graph all tweets
#-------------------------------------------------------------
words = ' '.join([text for text in df['text']])
wordcloud = WordCloud(
    width=800, height=400, background_color='white', max_font_size=110).generate(words)
plt.figure(figsize=(14, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.title('Words in all tweet\n', fontsize=24)
plt.axis('off')
plt.show()


# graph list of words except for Ticker
#-------------------------------------------------------------
not_ticker = [] # list of words except for Ticker
for text in df['text']:
    for word in text.split():
        if word.upper() not in ticker_dic:
            not_ticker.append(word)
            
words = ' '.join([word for word in not_ticker])
wordcloud = WordCloud(
    width=800, height=400, background_color='white', max_font_size=110).generate(words)

plt.figure(figsize=(14, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.title('Words in all tweet without Ticker\n', fontsize=24)
plt.axis('off')
plt.show()


def wordcloud_by_sentiment(sentiment):
    not_ticker = []

    for text in df[df['sentiment']==sentiment]['text']:
        for word in text.split():
            if word.upper() not in ticker_dic:
                not_ticker.append(word.lower())

    words = ' '.join([word for word in not_ticker])
    wordcloud = WordCloud(
        width=800, height=400, background_color='white', max_font_size=110, max_words=100).generate(words)
    
    plt.figure(figsize=(14, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title('Words in '+ sentiment.capitalize() + ' tweets\n', fontsize=32)
    plt.axis('off')
    plt.show()
    
    
wordcloud_by_sentiment(_positive)
wordcloud_by_sentiment(_negative)
wordcloud_by_sentiment(_neutral)    