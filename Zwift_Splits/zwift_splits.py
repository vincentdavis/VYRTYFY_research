

def check_split_times(t0, t1, global_splits, roadTime_radius=2000, xy_radius=480000):
        """
            two concecutive rider data points  t0 and t1 as a dict.
            all_splits = custom/privet event splits and Global splits
            global splits is a dict of splits like:
            {'Finish': {'x':123, 'y':345, 'roadTime':809292},
             'KOM': {'x':123, 'y':345, 'roadTime':103876},
            }
            """
        rt0 = t0['roadTime']
        x0 = t0['x']
        y0 = t0['y']
        rt1 = t1['roadTime']
        x1 = t0['x']
        y1 = t0['y']

        for name, split in global_splits.items():  # filter for splits near the points
            try:
                near_rt = (abs(split['roadTime'] - rt0) <= roadTime_radius) and (
                            abs(split['roadTime'] - rt1) <= roadTime_radius)
                near_xy = (((split['x'] - x0)**2 + (split['y'] - y0)**2) <= xy_radius**2) and (
                          ((split['x'] - x1)**2 + (split['y'] - y1)**2) <= xy_radius**2)
                if near_rt and near_xy: #not sure if this should be an "or" or "and"
                    # check if we passed the point from to > t1
                    crossed_up = rt0 <= split['roadTime'] <= rt1  # increasing roadTime
                    crossed_down = rt1 <= split['roadTime'] <= rt0  # decreasing roadTime
                    if (crossed_up or crossed_down):
                        # print(((split['x'] - x0)**2 + (split['y'] - y0)**2)**.5, ((split['x'] - x1)**2 + (split['y'] - y1)**2)**.5)
                        # Interpolate
                        slope = (t1['irlTime'] - t0['irlTime']) / (rt1 - rt0)
                        split_time = slope * (split['roadTime'] - rt0) + t0['irlTime']
                        print(
                            f"Check:\n{rt0} > {split['roadTime']} > {rt1}\n{t0['irlTime']} > {split_time} > {t1['irlTime']}")
                        return {'id': t0['id'], 't0':t0, 't1':t1, 'split_time': split_time, 'split_name': name, 'split_data': split, 'metrics': {}}
            except Exception as e:
                # should log something
                print(f"****Error\nSplit Name:{name}\nt0: {t0}\nt1: {t1}")
                # print(e)
                raise e
                # return {'error': {'id': t0['id'], 'split_name': name, 'split_data': split}}

