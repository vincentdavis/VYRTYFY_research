from datetime import datetime
import json
import pandas as pd
import numpy as np

def world_time_to_timestamp(world_time):
    return datetime.fromtimestamp((int(world_time) + 1414016075000) / 1000.0)

def multiple_id_reader(json_path, start_time):
  with open(json_path) as j:
    data = json.load(j)
  row_list = []
  for id, id_data in data.items():
    # print(id)
    if id_data is not None:
          for row in id_data.values():
            row.update({'id':id})
            row_list.append(row)
  df = pd.DataFrame(row_list)
  event_start_time = np.datetime64(start_time)
  df['worldTime_1'] = df['worldTime']
  df['irlTime'] = pd.to_datetime(df['worldTime'], unit='ms')
  df['irlTime'] = df['worldTime'] + pd.Timedelta(seconds = (1414016075))

  df.sort_values(by=['irlTime'], inplace=True)
  df = df.reset_index(drop=True)
  df['y'] = -df.y
  df = df[['id', 'distance', 'heading', 'heartrate', 'power', 'progress', 'roadTime', 'speed', 'time', 'timestamp', 'worldTime', 'worldTime_1', 'irlTime', 'x', 'y', 'groupId', 'laps']]
  return df

def single_id_json(data_file):
    """ retunrs a list of json records"""

    with open(data_file) as j:
        data = [d for d in json.load(j).values()]
        data2 = []
        for d in data:
            if 'irlTime' not in d.keys(): #Newer data may have this
                d.update({'irlTime':world_time_to_timestamp(d['worldTime'])})
                data2.append(d)
    return data2



