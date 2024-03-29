import pandas as pd
data_clean = pd.read_csv(r"D:\Tel U\Semester 6\TCC\data_hasil_TextPreProcessing.csv")

import re
def praproses(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)()(?:-)?(?:\)|\(|D|P)',
                           text)
    text = (re.sub('[\W]+', ' ', text.lower()) +
            ' '.join(emoticons).replace('-', ''))
    return text

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data_clean['content'], data_clean['Label'],
                                                    test_size = 0.20,
                                                    random_state = 0)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer()
tfidf_train = tfidf_vectorizer.fit_transform(X_train)
tfidf_test = tfidf_vectorizer.transform(X_test)

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
vectorizer.fit(X_train)

X_train = vectorizer.transform(X_train)
X_test = vectorizer.transform(X_test)

from sklearn.naive_bayes import MultinomialNB

nb = MultinomialNB()
nb.fit(tfidf_train, y_train)

X_train.toarray()

y_pred = nb.predict(tfidf_test)

from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud  # Menambahkan impor WordCloud

# Load dataset
def load_data():
    return pd.read_csv('data_hasil_TextPreProcessing.csv')

def load_data_user():
    return pd.read_csv('data_awal.csv')

def display_wordcloud(data):
    tokenized_text = ' '.join(data['content'])
    wordcloud = WordCloud(width=300, height=150, background_color ='white').generate(tokenized_text)
    plt.figure(figsize=(6, 3))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('WordCloud of Most Frequent Words')
    st.image(wordcloud.to_array(), caption='WordCloud', use_column_width=True)

def display_sentiment_distribution(data):
    sentiment_counts = data['Label'].value_counts()

    fig_sentiment = px.pie(sentiment_counts, values=sentiment_counts.values, names=sentiment_counts.index,
                           title='Sentiment Distribution')
    return fig_sentiment

def display_time_distribution(data_user):
    data_user['at'] = pd.to_datetime(data_user['at'])
    time_distribution = data_user['at'].dt.hour.value_counts().sort_index()

    fig_time_distribution = px.line(time_distribution, x=time_distribution.index, y=time_distribution.values,
                                    labels={'x': 'Hour', 'y': 'Count'}, title='Time Distribution')
    return fig_time_distribution

# Function to display top 5 comments with most thumbsUpCount
def display_top_comments(data_user):
    top_comments = data_user.nlargest(5, 'thumbsUpCount')[['userName', 'content', 'thumbsUpCount']]
    return top_comments

# Function to display bar chart for top 5 comments with most thumbsUpCount
def display_top_comments_bar_chart(top_comments):
    fig_top_comments = px.bar(top_comments, x='userName', y='thumbsUpCount', text='content',
                              labels={'thumbsUpCount': 'ThumbsUpCount', 'userName': 'User'},
                              title='Top 5 Comments with Most ThumbsUpCount')
    fig_top_comments.update_traces(texttemplate='%{text}', textposition='outside')
    fig_top_comments.update_layout(xaxis_title='User', yaxis_title='ThumbsUpCount', height=400)
    return fig_top_comments

# Function to display sentiment with most thumbsUpCount as pie chart
def display_sentiment_with_most_thumbsup_piechart(data_user):
    sentiment_thumbsup = data_user.groupby('score')['thumbsUpCount'].sum().reset_index()
    fig_sentiment_thumbsup = px.pie(sentiment_thumbsup, values='thumbsUpCount', names='score',
                                    title='Sentiment with Most ThumbsUpCount')
    fig_sentiment_thumbsup.update_layout(height=300, width=400)
    return fig_sentiment_thumbsup

# Function to display score distribution
def display_score_distribution(data_user):
    score_distribution = data_user['score'].value_counts().reset_index().rename(columns={'index': 'score', 'score': 'count'})
    fig_score_distribution = px.pie(score_distribution, values='count', names='score',
                                    title='Score Distribution')
    fig_score_distribution.update_layout(height=300, width=400)
    return fig_score_distribution

# Main function
def main():
    st.title('App Review Sentiment Analysis')

    # Load data
    data = load_data()
    data_user = load_data_user()

    top_row, bottom_row = st.columns(2)

    with top_row:
        st.header('Sentiment Distribution')
        fig_sentiment = display_sentiment_distribution(data)
        st.plotly_chart(fig_sentiment)

        st.header('Time Distribution')
        fig_time_distribution = display_time_distribution(data_user)
        st.plotly_chart(fig_time_distribution)

        st.header('WordCloud of Most Frequent Words')
        display_wordcloud(data)

    with bottom_row:
        st.header('Top 5 Comments with Most ThumbsUpCount')
        top_comments = display_top_comments(data_user)
        st.dataframe(top_comments)

        st.header('Bar Chart for Top 5 Comments with Most ThumbsUpCount')
        fig_top_comments = display_top_comments_bar_chart(top_comments)
        st.plotly_chart(fig_top_comments)

        st.header('Sentiment with Most ThumbsUpCount')
        fig_sentiment_thumbsup = display_sentiment_with_most_thumbsup_piechart(data_user)
        st.plotly_chart(fig_sentiment_thumbsup)

        st.header('Score Distribution')
        fig_score_piechart = display_score_distribution(data_user)
        st.plotly_chart(fig_score_piechart)

if __name__ == '__main__':
    main()
