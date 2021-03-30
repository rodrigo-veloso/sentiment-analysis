
import streamlit as st

col1, col2 = st.beta_columns((2,1))

col1.write("""# Análise de sentimento""")

col2.image('a3.png', width =60)


st.write("""Utilizando modelos de processamento de linguagem natural e dados de texto do Twitter elaboramos uma aplicação que dada uma palavara de interesse é possível medir o sentimento atual relativo à aquela palavra.""")

import tweepy as tw
from leia import SentimentIntensityAnalyzer 
import pandas as pd
import seaborn as sns

def get_sentiment(score):
    if score['compound'] > 0.05:
        score['sentiment'] = 'Positivo'
    elif score['compound'] < -0.05:
        score['sentiment'] = 'Negativo'
    else:
        score['sentiment'] = 'Neutro'

def get_probabilities(scores):
    pos_count = 0
    neg_count = 0
    neu_count = 0
    total_score = 0
    for score in scores:
        total_score+=score['compound']
        if score['sentiment'] == 'Positivo':
            pos_count+=1
        elif score['sentiment'] == 'Negativo':
            neg_count+=1
        else:
            neu_count+=1
    return pos_count/len(scores), neg_count/len(scores), neu_count/len(scores), total_score/len(scores)

def get_probabilities_(scores):
    pos_count = 0
    neg_count = 0
    neu_count = 0
    total_score = 0
    for score in scores.iloc:
        total_score+=score['compound']
        if score['sentiment'] == 'Positivo':
            pos_count+=1
        elif score['sentiment'] == 'Negativo':
            neg_count+=1
        else:
            neu_count+=1
    return pos_count/len(scores), neg_count/len(scores), neu_count/len(scores), total_score/len(scores)

def f(x):
    if x == 'positive':
        return 'Positivo'
    if x == 'negative':
        return 'Negativo'
    if x == 'neutral':
        return 'Neutro'

s = SentimentIntensityAnalyzer()

word = st.text_input('Digite uma palavra')

if word:

    consumer_key = 'F5ucChFt93smoSFH8UGA9Qxph'
    consumer_secret = 'Skqf43paBcoQJIkcoamD8Q7t4pyQlLXib6RYkQLpC65Nl40ths'
    access_token = '1376534696021131268-iKSpA7AoTF263diuEFMdr1bK0KWE2q'
    access_token_secret = 'jbuJPeQkHyfPdm2D7mvIQChki0hKYsXClD2slPtFjmcDf'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth,wait_on_rate_limit=True)
    public_tweets = api.home_timeline()

    tweets = tw.Cursor(api.search,q=word).items(1000)

    scores = []
    with st.spinner(text='Carregando dados do Twitter...'):

        for tweet in tweets:
            if tweet.metadata['iso_language_code'] == 'pt':
                #print(tweet.text)
                data = s.polarity_scores(tweet.text)
                data['text'] = tweet.text
                scores.append(data)
        st.success('Done')

    for score in scores:
        get_sentiment(score)
    pos,neg,neu,avg = get_probabilities(scores)
    data = pd.DataFrame(scores)
    #data = pd.read_csv('data.csv',index_col=0)
    #data['sentiment'] = data['sentiment'].apply(lambda x: f(x))
    sns.set(font_scale = 1.3)
    plt = sns.catplot(data = data, x = 'sentiment',kind="count", aspect = 1.8, palette = "mako")
    plt.set_axis_labels("Sentimento","Quantidade")
    st.pyplot(plt)
    #st.write("""Percentual de negativos: {}""".format(neg))
    #st.write(data['sentiment'])
    #pos,neg,neu,avg = get_probabilities_(data)
    st.write("""### Percentual de negativos: {:.2f}%""".format(neg*100))
    st.write("""### Percentual de positivos: {:.2f}%""".format(pos*100))
    st.write("""## Exemplos de tweets positivos""")
    data = data.sort_values(by='compound', ascending=False, ignore_index = True)
    st.write("""### "{}" """.format(data['text'][0]))
    st.write("""### "{}" """.format(data['text'][1]))
    st.write("""### "{}" """.format(data['text'][2]))
    st.write("""## Exemplos de tweets negativos""")
    st.write("""### "{}" """.format(data['text'][len(data)-1]))
    st.write("""### "{}" """.format(data['text'][len(data)-2]))
    st.write("""### "{}" """.format(data['text'][len(data)-3]))
