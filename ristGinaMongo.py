import pandas as pd

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

    df = pd.DataFrame(data)
    
    df[key_str] = pd.to_datetime(df[key_str], utc=True)
    df.set_index(key_str, inplace=True)
    df.index = df.index.tz_convert('Europe/Rome')

    return df