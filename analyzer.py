import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_happiness_per_month(data, id):

    """
    Getting mean, percent and sum happiness level per each month for id

    Args:
        data (DataFrame) - DataFrame of messages
        id (int) - user id for analyze, if is None use all

    Return
        Dict like this
        {
            'date': []
            'mean_happiness': []
            'percent_happiness': []
            'sum_happiness': []
        }
    """

    if id is not None:
        data = data.loc[data.loc[:, 'from_id'] == id]
    data = data.sort_values(by='datetime').reset_index()
    first_d = data.loc[0, 'datetime'].to_pydatetime().replace(day=1).date()
    end_d = data.loc[data.shape[0]-1, 'datetime'].to_pydatetime().date()
    curr_d = first_d
    res = {
            'date': [],
            'mean_happiness': [],
            'percent_happiness': [],
            'sum_happiness': [],
           }
    while curr_d < end_d:
        new_data = data.loc[(curr_d.month == data.loc[:, 'datetime'].dt.month) &
                            (curr_d.year == data.loc[:, 'datetime'].dt.year), :]
        res['date'].append(curr_d)
        res['mean_happiness'].append(new_data['happiness'].mean())
        res['percent_happiness'].append(new_data.loc[new_data['happiness'] != 0, 'happiness'].count() / new_data.shape[0])
        res['sum_happiness'].append(new_data['happiness'].sum())
        curr_d = curr_d + relativedelta(months=+1)
    return res


def get_happiness_per_user(data, diags, id):
    """
    Getting mean and percent happiness for each user

    Args:
        data (dataframe) - DataFrame of messages
        diags - dict of diags:
        {
            'id':[]
            'name':[]
            'total_msgs':[] 
            'is_user':[]
            'is_group':[]
            'is_channel'
        } 
        id (int) - id to analize

    Returns:
        Dict like this
        {
            'user_id': [],
            'full_name': [],
            'mean_happiness': [],
            'percent':[]
        }
     """

    res = {
          'user_id': [],
          'full_name': [],
          'mean_happiness': [],
          'percent':[]
          }
    if id is not None:
        data = data.loc[data.loc[:, 'from_id'] == id]
    df_diags = pd.DataFrame(diags)
    for to_id in data['to_id'].unique():
        new_data = data.loc[data['to_id']==to_id,:].reset_index()
        res['user_id'].append(to_id)
        res['full_name'].append(df_diags.loc[df_diags['id']==to_id,'name'].iloc[0])
        res['mean_happiness'].append(new_data['happiness'].mean())
        res['percent'].append(new_data.loc[new_data['happiness']!=0,'happiness'].count()
                              / new_data.shape[0])
    return res


def get_happiness_per_hours(data, id, timezone='Europe/Moscow'):
    """
    Getting mean and percen happiness per any hour in day

    Args:
        data (dataframe) - DataFrame of messages
        timezone (str) - timezone to correct msgs time
        id (int) - id of user to analyze

    Returns:
        Dict
        {
            'hours':[0,1,...,23]
            'mean_happiness':[]
            'percent_happiness':[]
        }
    """
    res = {
            'hours': [],
            'mean_happiness': [],
            'percent_happiness': []
           }
    if id is not None:
        data = data.loc[data.loc[:, 'from_id'] == id]
    data['datetime'] = data['datetime'].dt.tz_convert(timezone)
    for hour in range(24):
        new_data = data.loc[data.loc[:,'datetime'].dt.hour == hour, :]
        res['hours'].append(hour)
        res['mean_happiness'].append(new_data['happiness'].mean())
        res['percent_happiness'].append(new_data.loc[new_data['happiness'] != 0, 'happiness'].count()
                                        / new_data.shape[0])
    return res
