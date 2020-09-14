# ZWIFT.COM TEAM TIME TRIALS

from datetime import timedelta
import pandas as pd
from haversine import haversine, Unit

def merge_activities(path, fix_time=None):
    """
    Data is imported and columns are named using the file name a field.
    For example Altitude_John
    :param path:
    :return: dataframe and names
    """
    df = pd.DataFrame()
    names = []
    for a in [f for f in path if f.is_file() and f.suffix=='.csv']:
      print("***",a)
      df_temp = pd.read_csv(a, parse_dates= ['Date_Time']).drop(['Unnamed: 0', 'No'], axis=1)
      name = a.stem
      if fix_time:
          df_temp['Date_Time'] = df_temp['Date_Time'] + timedelta(seconds=fix_time[name])
      names.append(name)
      # print(name)
      df_temp.rename(columns={'Latitude': f'Latitude_{name}',	'Longitude': f'Longitude_{name}', 'Altitude': f'Altitude_{name}',
                              'Speed': f'Speed_{name}', 'Heartrate': f'Heartrate_{name}', 'Cadence': f'Cadence_{name}',
                              'Power': f'Power_{name}'}, inplace=True)
      if len(df) == 0:
        df = df_temp.copy()
      else:
        df = pd.merge(df, df_temp, on='Date_Time')
    return df, names

def rolling_metrics(df, names, hr=True, exclude=None, periods =[30, 60, 300, 1200]):
    """
    Calculates 30sec, 1min, 5min 20min rolling/moving averages
    Calculates max and min of each rolling average
    Sometimes we are missing heartrate, so we can exlude that.
    we allow for dropped or missing data, 10%
    :param df:
    :return: df and dict like {name:{metric:value},}
    """
    stats = {}
    for n in names:
        nd = stats[n] = {}
        for p in periods:
            temp = df[60:-60][f'Power_{n}'].rolling(p, min_periods=int(p*.9)).mean()
            nd[f'w{p}min'] = temp.min()
            nd[f'w{p}max'] = temp.max()
            if hr:
                temp = df[60:-60][f'Heartrate_{n}'].rolling(p, min_periods=int(p * .9)).mean()
                nd[f'hr{p}min'] = temp.min()
                nd[f'hr{p}max'] = temp.max()
    return stats

def team_position(df, names):
    from haversine import haversine
    lat = [lat for lat in df.columns if lat.split('_')[0] == 'Latitude']
    lon = [lon for lon in df.columns if lon.split('_')[0] == 'Longitude']
    df['lat_center'] = df[lat].mean(axis=1)
    df['lon_center'] = df[lon].mean(axis=1)
    for n in names:
        df[f'{n}_to_center'] = df[['lat_center', 'lon_center', f"Latitude_{n}", f"Longitude_{n}"]].apply(
            lambda x: haversine((x[0], x[1]), (x[2], x[3]), unit=Unit.METERS), axis=1)
    return df

def distance(df):
    """
    flat distacnce ignores elevation
    :return: {'total_distance': total_distance}
    """
    df["shift_lon_center"] = df.shift(1)["lon_center"]
    df["shift_lat_center"] = df.shift(1)["lat_center"]
    # This is the flat distance between points
    df["distance_between"] = df[['lat_center', 'lon_center', 'shift_lat_center', "shift_lon_center"]].apply(
        lambda x: haversine((x[0], x[1]),(x[2], x[3]), unit=Unit.METERS), axis=1)
    df.drop(['shift_lon_center', 'shift_lat_center'], axis=1)
    total_distance = df["distance_between"].sum()
    df['distance'] = df['distance_between'].cumsum()
    mean_dist = df[df.distance_between > 0]["distance_between"].mean()
    median_dist = float(df[df.distance_between > 0]["distance_between"].median())
    max_dist = df["distance_between"].max()
    min_dist = df[df.distance_between > 0]["distance_between"].min()
    return {'total_distance': total_distance,
            'mean_dist': mean_dist,
            'median_dist': median_dist,
            'max_dist': max_dist,
            'min_dist': min_dist,
            'df':df
            }
