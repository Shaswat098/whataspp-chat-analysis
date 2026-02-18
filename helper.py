import emoji
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter


def fetch_stats(selected_user, df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    # fetch number of messages
    num_messages =  df.shape[0]

    # fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        extractor = URLExtract()
        links.extend(extractor.find_urls(message))
    
    return num_messages, words, num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts() / df.shape[0] * 100).reset_index().rename(columns = {'user' : 'Name', 'count' : 'Percent'})
    return x, df

def create_wordcloud(selected_user, df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500,
                    height=500,
                    min_font_size=10,
                    background_color='white'
                )
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    temp = df[(df['user'] != 'system') & (df['message'] != '<Media omitted>')]
    words = []
    for message in temp['message']:
        for word in message.split():
            words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    if len(emojis) == 0:
        return pd.DataFrame()

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    df['month_num'] = df['date'].dt.month
   
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date  

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    user_heatmap = df.pivot_table(index='day_name',
                                   columns='hour',
                                   values='message',
                                   aggfunc='count').fillna(0)
    return user_heatmap