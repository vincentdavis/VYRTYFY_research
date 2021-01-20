from datetime import datetime
from data_generator import multiple_id_reader
from zwift_splits import splits
from global_splits import split_loc

def test_splits_1():
  data_file = 'data/BRAC Jan 16 2021 all riders.json'
  start_time = datetime.strptime('2021-01-09 16:05', '%Y-%m-%d %H:%M')
  df = multiple_id_reader(data_file, start_time)
#   df.to_json('data/BRAC_jan_16_records.json', orient='records')
  for id in df.id.unique():
    print("****")
    rider_data_list = df[df.id==id].to_dict('records')
    count = len(rider_data_list)
    for idx in range(count):
      if idx <= count-2:
        t0 = rider_data_list[idx]
        t1 = rider_data_list[idx+1]
        splits(t0, t1, split_loc)

def test_splits_json():
    data_file = 'data/BRAC_jan_16_records.json'
    with open(data_file) as j:
        data = json.load(j)
    for record in data:
        # send to cache
        pass

test_splits_1()