import pandas as pd
from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import numpy as np
from collections import Counter
import emoji
import re

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch url from messages
    url = []
    for message in df['message']:
        url.extend(extractor.find_urls(message))




    return num_messages, len(words), num_media_messages,len(url)

def most_busy_users(df):
    temp = df[df['user'] != 'group_notification']

    X = temp['user'].value_counts().head(6)
    user_m_per = round((temp['user'].value_counts().head(6) / df.shape[0]) * 100, 2).reset_index().rename(columns={"count": "percentage"})
    return X, user_m_per



def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(collocations=False, background_color='white',width=2048, height=1080)
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc



def most_common_word(selected_user, df):
    f = open(r'stop_hinglish.txt', 'r')
    stop_word = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002700-\U000027BF"  # Dingbats
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U0001F700-\U0001F77F"  # Alchemical Symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002500-\U00002BEF"  # Chinese characters
        "\U0000200D"  # Zero Width Joiner
        "\U0000231A-\U0000231B"  # Miscellaneous Technical
        "\U00002B05-\U00002B07"  # Arrows
        "\U00003030-\U0000303F"  # CJK Symbols and Punctuation
        "]+", flags=re.UNICODE
    )

    def extract_emojis(text):
        return emoji_pattern.findall(text)

    df['emoji'] = df['message'].apply(extract_emojis)
    temp = df[df['emoji'].map(bool)]
    emoji = temp['emoji']
    data = pd.DataFrame(emoji).reset_index(drop=True)
    return data

def monthly_time_line(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'Month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_time_line(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # df.groupby(['daily']).count()['message']
    weekly_activity = df['daily'].value_counts()
    return weekly_activity
def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    monthly_activity = df['month'].value_counts()
    return monthly_activity

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    user_heatmap = df.pivot_table(index='daily', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap










