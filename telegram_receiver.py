from telethon import TelegramClient, sync
from telethon import errors


def telegram_start(session_name, api_id, api_hash):
    """
    Sing-in to telegram

    Args:
        session_name: session name for telegram
        api_id: Telegram Api Id
        api_hash: Telegram Api Hash

    Return:
        Dictionary with inform of me, if unsucsess return None
        {
            'id' : id (int)
            'username' : username (str)
            'first_name' : first name (str)
            'last_name' : last name (str)

        }
    """    
    try:
        client = TelegramClient(session_name, api_id, api_hash).start()
        me = client.get_me()
        return {
                'id' : me.id,
                'username': me.username,
                'first_name': me.first_name,
                'last_name': me.last_name
               }
    except errors.FloodWaitError as e:
        print('Flood, need waiting', e.message)
        return (None)
    except errors.ApiIdInvalidError:
        print("Unsuccessful sign-in! Wrong API.")
        return (None)
    except ConnectionError:
        print("No internet")
        return (None)
    finally:
         client.disconnect()


def get_msgs (session_name, api_id, api_hash, diag_lim=0, msg_lim=None, from_user=True, from_group=False, msg_count_lim=None):

    """
    Get telegram messages from id or all messages if id is None

    Args: 
        session_name: session name for telegram
        api_id: Telegram Api Id
        api_hash: Telegram Api Hash
        diag_lim (int)- use it to limit receive diag
        msg_lim (int)- msg lim to get in each diag
        from_user (bool) - receive message from  users, not group or channel
        from_group (bool) - receive message from  group, not user or channel
        msg_count_lim (int) - minimum messages in chat to get it

    returns:
        Dict of messages lists:
        {
        'datetime': [],
        'id': [],    
        'from_id': [],
        'to_type': [],
        'to_id': [],
        'text': [],
        'is_forwarded': [],
        'has_sticker': [],
        'has_video': [],
        'has_voice': [],
        'has_photo': []
        }
        
    """
    client = TelegramClient(session_name,api_id,api_hash)
    client.connect()
    me = client.get_me()
    status = 0
    status_check = 1000
    msgs = {
        'datetime': [],
        'id': [],    
        'from_id': [],
        'to_type': [],
        'to_id': [],
        'text': [],
        'is_forwarded': [],
        'has_sticker': [],
        'has_video': [],
        'has_voice': [],
        'has_photo': []
        }

    for diag in client.iter_dialogs(limit=diag_lim):
        total = client.get_messages(diag).total
        print('Total messges with', diag.name, 'is', total)
        if total >= msg_count_lim:
            if ((diag.is_user and from_user) or (diag.is_group and from_group))\
                    and me.first_name not in diag.name:
                try:
                    for msg in client.iter_messages(diag, limit=msg_lim):
                        dest = msg.to_id.to_dict()
                        msgs['datetime'].append(msg.date)
                        msgs['id'].append(msg.id)
                        msgs['from_id'].append(msg.from_id)
                        msgs['to_type'].append(list(dest.keys())[1])
                        msgs['to_id'].append(dest[list(dest.keys())[1]])
                        msgs['text'].append(msg.message)
                        msgs['is_forwarded'].append(msg.forward is not None)
                        msgs['has_sticker'].append(msg.sticker is not None)
                        msgs['has_video'].append(msg.video is not None)
                        msgs['has_voice'].append(msg.voice is not None)
                        msgs['has_photo'].append(msg.photo is not None)
                        status += 1
                        if status % status_check == 0:
                            print ('...loading {:.2%} messages'.format(status/total))
                    status = 0
                    print('Messages get succesfully from',diag.name)
                except errors.ChatAdminRequiredError as e:
                    print('Messages cant get from',diag.name, e.mesasage)
                except errors.FloodWaitError as e:
                    print('Messages cant get from',diag.name, e.mesasage)
            else:
                print(diag.name, 'is not user or group')
        else:
            print(diag.name, 'had messages less limit')
                       
    client.disconnect()
    total_msg = len(msgs['id'])
    print('Total get',total_msg,'messages') 
    return msgs    


def get_diags(session_name, api_id, api_hash):
    """
    Geting dialogs list

    Args:
        session_name: session name for telegram
        api_id: Telegram Api Id
        api_hash: Telegram Api Hash

    Returns:
        dict of diags:
        {
            'id':[],
            'name':[],
            'total_msgs':[],
            'is_user':[],
            'is_group':[],
            'is_channel':[],
        } 
    """
    diags = {
            'id': [],
            'name': [],
            'total_msgs': [],
            'is_user': [],
            'is_group': [],
            'is_channel': []
        } 
    client = TelegramClient(session_name,api_id,api_hash)
    client.connect()
    for diag in client.iter_dialogs():
        diags['id'].append(diag.id)
        diags['name'].append(diag.name)
        diags['total_msgs'].append(client.get_messages(diag).total)
        diags['is_user'].append(diag.is_user)
        diags['is_group'].append(diag.is_group)
        diags['is_channel'].append(diag.is_channel)
    client.disconnect()
    return (diags)

