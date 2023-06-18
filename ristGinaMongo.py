import pytz
from dateutil import tz
from zoneinfo import ZoneInfo


def get_last_log(client, collection):
    db = client['CF01']
    collection = db[collection]

    last_document = collection.find_one(sort=[('_id', -1)])

    if last_document:
        logTime = pytz.utc.localize(last_document['logTime'])
        logTime = logTime.astimezone(ZoneInfo("Europe/Rome"))
        temp = last_document['temp']
    else:
        logTime = 'not found'
        temp = 'not found'
    
    return logTime, temp


def get_data_timerange(client, collection, start_date, end_date):
    
    if collection == 'errors':
        key_str = 'errTime'
        value_str = 'errStr'
    elif collection == 'logs':
        key_str = 'logTime'
        value_str = 'temp'
    elif collection == 'messages':
        key_str = 'msgTime'
        value_str = 'msgStr'
    elif collection == 'updates':
        key_str = 'updateTime'
        value_str = 'updateStr'
    else:
        raise Exception('Error::: get_data_timerange()')
    
    db = client['CF01']
    collection = db[collection]
    
    query = {
        key_str: {
            "$gte": start_date,
            "$lte": end_date
        }
    }

    projection = {
        "_id": 0,
        key_str: 1,
        value_str: 1
    }

    cursor = collection.find(query, projection)
    data = list(cursor)

    x, y = [], []
    for i in data:
        x.append(i['logTime'])
        y.append(i['temp'])
    
    return x, y
