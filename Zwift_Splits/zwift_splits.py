

def splits(t0, t1, global_splits):
    """
    two concecutive rider data points  t0 and t1 as a dict.
    all_splits = custom/privet event splits and Global splits
    """
    # Setup
    roadTime_radius = 2000 # roadTime unit
    # x_radius = 2000
    # x_radius = 2000
    rt0 = t0['roadTime']
    rt1 = t1['roadTime']
    for name, split in global_splits.items(): # filter for splits near the points
        try:
            near_rt = (abs(split['roadTime'] - rt0) <= roadTime_radius) and (abs(split['roadTime'] - rt1) <= roadTime_radius)
            if near_rt:
                # check if we passed the point from to > t1
                crossed_up = rt0 <= split['roadTime'] <= rt1 # increasing roadTime
                crossed_down = rt1 <= split['roadTime'] <= rt0 # decreasing roadTime
                if (crossed_up or crossed_down):
                    # Interpolate
                    slope = (t1['zwiftTime'] - t0['zwiftTime'])/(rt1 - rt0)
                    split_time = slope * (split['roadTime'] - rt0) + t0['zwiftTime']
                    print(f"Check:\n{rt0} > {split['roadTime']} > {rt1}\n{t0['zwiftTime']} > {split_time} > {t1['zwiftTime']}")
                    return {'id':t0['id'], 'split_time': split_time, 'split_name': global_splits[name], 'split_data':split, 'metrics':{}}
        except:
            # should log something
            print(f"****Error\nSplit Name:{name}\nt0: {t0}\nt1: {t1}")
            return {'error': {'id':t0['id'], 'split_name':name, 'split_data':split}}
