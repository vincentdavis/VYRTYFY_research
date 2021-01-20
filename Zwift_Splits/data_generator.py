import datetime
import json
import pandas as pd
import numpy as np

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
  df['worldTime'] = pd.to_datetime(df['worldTime'], unit='ms')
  df['zwiftTime'] = df['worldTime'] + pd.Timedelta(seconds = (1414016075))

  df.sort_values(by=['zwiftTime'], inplace=True)
  df = df.reset_index(drop=True)
  df['y'] = -df.y
  df = df[['id', 'distance', 'heading', 'heartrate', 'power', 'progress', 'roadTime', 'speed', 'time', 'timestamp', 'worldTime', 'worldTime_1', 'zwiftTime', 'x', 'y', 'groupId', 'laps']]
  return df


