
from subprocess import call
import xarray as xr
import pandas as pd
import os
import numpy as np


def preprocess_n100(n100_raw, n100_processed, processed_info):
    """
       Create well structured csv files from n100 data. Output has
       date as index and n100 concentration as the other column.
    """
    make_directory(n100_processed)
    initial_info = 'Measurementsites_info.txt'
    preprocess_n100_info(n100_raw, n100_processed, initial_info, processed_info)
    cities = pd.read_csv(processed_info)
    for city in cities['city']:
        preprocess_n100_file(n100_raw, n100_processed, city)

def preprocess_n100_info(n100_raw, n100_processed, initial_info, processed_info):
    """
       Create an info file for the cities containing their name id and 
       location in lat long degrees.
    """
    info = []
    with open(n100_raw + '/' + initial_info, 'r') as f:
        for line in f:
            if '%' in line:
                continue
            line = line.split()
            line = [elem.strip(',') for elem in line][:4]
            info.append(dict(city=line[3], latitude=line[0], longitude=line[1]))
    pd.DataFrame(info).to_csv(processed_info, index=False)
    

def preprocess_n100_file(n100_raw, n100_processed, city):
    """
       Merge separate time columns into one date index.
    """
    columns = ['year', 'month', 'day', 'hour', 'minute', 'concentration']
    df = pd.read_csv(n100_raw + '/' + city + '_N100.dat', names=columns, header=None, delim_whitespace=True)
    df = df.set_index(pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']]))
    df = df.drop(columns=['year', 'month', 'day', 'hour', 'minute'])
    df = df.groupby(df.index.date).mean()
    df.index.name = 'date'
    df.to_csv(n100_processed + '/' + city + '_N100.csv')

def preprocess_cams(cams_raw, cams_processed, cities_info):
    """
       Create csv files from CAMS reanalysis GRIB files. Output contains
       temperature (t) and carbon monoxide (co), date act as index.
    """
    make_directory(cams_processed)
    cities = pd.read_csv(cities_info)
    for index, row in cities.iterrows():
        city = row['city']
        latitude = row['latitude']
        longitude = row['longitude']
        if longitude < 0: longitude = longitude + 360
        files = listdir_fullpath(cams_raw + '/' + city)
        files = [f for f in files if ('.idx' not in f) and (city + '.grb' not in f)]
        outgrib = cams_raw + '/' + city + '/' + city + '.grb'
        concat_files(files, outgrib)
        ds = xr.open_dataset(outgrib, engine='cfgrib')
        df = ds.loc[dict(latitude=latitude, longitude=longitude)].to_dataframe()
        df = df.groupby(df.index.date).mean()
        df = df.drop(columns=['hybrid', 'latitude', 'longitude'])
        df.index.name = 'date'
        df.to_csv(cams_processed + '/' + city + '_CAMS.csv')

def make_directory(location):
    """
       Creates directory, no error if existing, make parent directories as needed.
    """
    call(['mkdir', '-p', location])

def concat_files(files, outfile):
    """
       Concatenate files to one outfile.
    """
    command = ['cat'] + files + ['>', outfile]
    call(' '.join(command), shell=True)

def listdir_fullpath(d):
    """
       Return a list of all files with their full paths in directory d.
    """
    return [os.path.join(d, f) for f in os.listdir(d)]

def unite_data(n100_data, cams_data, cities_info, final_data):
    """
       Merge together n100 data and cams data where they share the same date index.
    """
    make_directory(final_data)
    for city in pd.read_csv(cities_info)['city']:
        n100 = pd.read_csv(n100_data + '/' + city + '_N100.csv', index_col='date')
        cams = pd.read_csv(cams_data + '/' + city + '_CAMS.csv', index_col='date')
        df = pd.concat([n100, cams], join='inner', axis=1)
        df.to_csv(final_data + '/' + city + '.csv')

def merge_final_files(cities_info, final_data):
    """
       Create a single data files from all cities' final data
    """
    col_names = ['date', 'city', 'latitude', 'longitude', 'concentration', 
                 't', 'co', 'no', 'no2', 'so2' , 'c10h16', 'c5h8']
    all = pd.DataFrame(columns = col_names)
    cities = pd.read_csv(cities_info)

    for i, row in cities.iterrows():
        city_name = row['city']
        data = pd.read_csv(final_data + '/' + city_name + '.csv')
        n = len(data.index)
        data = data.assign(city = pd.Series(np.repeat(city_name, n)))
        data = data.assign(latitude = pd.Series(np.repeat(row['latitude'], n)))
        data = data.assign(longitude = pd.Series(np.repeat(row['longitude'], n)))
        all = all.append(data)

    all = all[col_names]
    all.to_csv(final_data + '/all_merged.csv', index = False)
