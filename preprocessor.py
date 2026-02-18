import re
import pandas as pd

def preprocess(data):
    pattern = r'^(\d{1,2}/\d{1,2}/\d{4}, \d{2}:\d{2}) - (.*)'

    rows = []

    lines = data.split('\n')  

    for line in lines:
        line = line.strip()
        match = re.match(pattern, line)

        if match:
            date = match.group(1)
            rest = match.group(2)

            if ': ' in rest:
                user, message = rest.split(': ', 1)
            else:
                user = 'system'
                message = rest

            rows.append([date, user, message])

    df = pd.DataFrame(rows, columns=['date', 'user', 'message'])

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %H:%M')

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
