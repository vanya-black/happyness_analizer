import pandas as pd
from telegram_receiver import telegram_start, get_msgs, get_diags
from analyzer import get_happiness_per_month, get_happiness_per_user, get_happiness_per_hours


DIAG_LIM = None
MSG_LIM = None
MSG_COUNT_LIM = 100


me = telegram_start(SESSION_NAME,API_ID,API_HASH)
if me is not None:
    msgs = get_msgs(session_name=SESSION_NAME, api_id=API_ID ,api_hash=API_HASH,
                    diag_id = None, diag_lim = DIAG_LIM, msg_lim = MSG_LIM, from_user = True,
                    from_group = False, msg_count_lim=MSG_COUNT_LIM
                    )
    diags = get_diags(api_id=API_ID, api_hash=API_HASH, session_name=SESSION_NAME)
else:
    print ("Can't sing in to Telegram")

df = pd.DataFrame(msgs)
#add happiness level
df.loc[:,'happiness'] = df.loc[:,'text'].str.count('\)')



