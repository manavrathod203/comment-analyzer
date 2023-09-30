# DO NOT TOUCH!!
"""
1. Total number of comments analyzed
2. No. of positive, neutral and negative and neutral comments out of total comments
3. Pie chart of sentiment analysis
4. seperate positive, negative and neutral comments and show them in three different tables 

SAVES EVERYTHING 
pie chart : sentiment_pie_chart.png
Dataframes in csv files : positive_comments.csv , negative_comments.csv , neutral_comments.csv

"""
import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
from youtube_comment_downloader import *
import sys
script_directory = os.path.dirname(os.path.abspath(__file__))

def get_comments(url):
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)
    text_comments = [[comment['text']] for comment in comments]
    return text_comments

def analyze_comments():
    text_comments = get_comments(url)
    
    sia = SentimentIntensityAnalyzer()

    positive_comments = []
    negative_comments = []
    neutral_comments = []

    for comment in text_comments:
        sentiment_score = sia.polarity_scores(comment[0])['compound']
        if sentiment_score > 0:
            positive_comments.append(comment)
        elif sentiment_score < 0:
            negative_comments.append(comment)
        else:
            neutral_comments.append(comment)
    
    total_comments = len(text_comments)
    num_positive_comments = len(positive_comments)
    num_negative_comments = len(negative_comments)
    num_neutral_comments = len(neutral_comments)

    print('Total number of comments analyzed:', total_comments)
    print('Number of positive comments:', num_positive_comments)
    print('Number of negative comments:', num_negative_comments)
    print('Number of neutral comments:', num_neutral_comments)

    # print('\nSentiment Analysis Pie Chart:')
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [num_positive_comments, num_negative_comments, num_neutral_comments]
    colors = ['#AEE2FF', '#FF6969', '#FEFF86']

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.axis('equal')
    plt.savefig('sentiment_pie_chart.png')
    # plt.show()
    
    # Save the pie chart as a PNG image

    display_comment_tables(positive_comments, negative_comments, neutral_comments)


def display_comment_tables(positive_comments, negative_comments, neutral_comments):
    positive_df = pd.DataFrame(positive_comments, columns=['Positive Comments'])
    positive_df.insert(0, "#", range(1, len(positive_df) + 1))
    negative_df = pd.DataFrame(negative_comments, columns=['Negative Comments'])
    negative_df.insert(0, "#", range(1, len(negative_df) + 1))
    neutral_df = pd.DataFrame(neutral_comments, columns=['Neutral Comments'])
    neutral_df.insert(0, "#", range(1, len(neutral_df) + 1))


    
    # print('Positive Comments:')
    # print(positive_df)

    # print('Negative Comments:')
    # print(negative_df)

    # print('Neutral Comments:')
    # print(neutral_df)

    # Save DataFrames as CSV files
    positive_df.to_csv('positive_comments.csv', index=False)
    negative_df.to_csv('negative_comments.csv', index=False)
    neutral_df.to_csv('neutral_comments.csv', index=False)

    
if len(sys.argv) != 2:
    print("Usage: python main.py <url>")
    sys.exit(1)

url = sys.argv[1]
# print(url)
analyze_comments()
