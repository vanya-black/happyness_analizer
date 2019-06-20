import os
import pandas as pd
from telegram_receiver import telegram_start, get_msgs, get_diags
from analyzer import get_happiness_per_month, get_happiness_per_user, get_happiness_per_hours
from api import API_HASH, API_ID, SESSION_NAME
import datetime as dt
import plotly as py
import plotly.graph_objs as go

DIAG_LIM = None
MSG_LIM = None
MSG_COUNT_LIM = 100

print("Load new messages or using exist CSV file? [y/n]:", end=' ')
comm = input().upper()
self_path = os.path.dirname(os.path.abspath(__file__))
me = telegram_start(SESSION_NAME, API_ID, API_HASH)

while True:
    if comm == 'Y':
        #me = telegram_start(SESSION_NAME, API_ID, API_HASH)
        print(me['id'])
        if me is not None:
            msgs = get_msgs(SESSION_NAME, API_ID, API_HASH, diag_lim=DIAG_LIM, msg_lim=MSG_LIM,
                            from_user=True, from_group=False, msg_count_lim=MSG_COUNT_LIM)
            diags = get_diags(api_id=API_ID, api_hash=API_HASH, session_name=SESSION_NAME)
        else:
            print("Can't sing in to Telegram")
            break
        df = pd.DataFrame(msgs)
        path_to_csv = self_path + '\\tg_msgs_' + dt.datetime.utcnow().strftime('%H%M%S_%d%m%Y') + '.csv'
        df.to_csv(path_to_csv, index=False)
        break
    if comm.upper() == 'N':
        csv_list = list(filter(lambda x: '.csv' in x, os.listdir(self_path)))
        if not csv_list:
            print('No CSV file in directory')
            comm = 'f'
        else:
            print('Choose file:')
            for ind in range(len(csv_list)):
                print(ind, csv_list[ind])
            try:
                choosed = int(input())
            except ValueError:
                print('Type number of files 0..n')
                choosed = -1
            while True:
                if 0 <= choosed < len(csv_list):
                    df = pd.read_csv(csv_list[choosed])
                    break
                else:
                    print('Choose file by number:', end=' ')
                    try:
                        choosed = int(input())
                    except ValueError:
                        print('Type number of files 0..n')
            break
    if not (comm == 'Y' or comm == 'N'):
        print("Load new messages or using exist? [y/n]:", end=' ')
        comm = input().upper()
#print(df.head())
df.loc[:, 'happiness'] = df.loc[:, 'text'].str.count('\)')

df['datetime'] = pd.to_datetime(df['datetime'])

monthly = get_happiness_per_month(df, me['id'])

mean_trace = go.Scatter(x=monthly['date'],
                        y=monthly['mean_happiness'],
                        name='mean happiness')

perc_trace = go.Scatter(x=monthly['date'],
                        y=monthly['percent_happiness'],
                        name='percent happiness')

d = [mean_trace, perc_trace]
py.offline.plot(d, filename='my_monthly_happiness', auto_open=True)

hourly = get_happiness_per_hours(df, me['id'])

mean_trace = go.Scatter(x=hourly['hour'],
                        y=hourly['mean_happiness'],
                        name='mean happiness')

perc_trace = go.Scatter(x=hourly['hour'],
                        y=hourly['percent_happiness'],
                        name='percent happiness')

# sum_trace = go.Scatter(x=hourly['hour'],
#                        y=hourly['sum_happiness'],
#                        name='summary happiness')

d = [mean_trace, perc_trace]
py.offline.plot(d, filename='my_hourly_happiness', auto_open=True)

