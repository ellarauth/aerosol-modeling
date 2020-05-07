
import signal
from subprocess import call
import pandas as pd
import calendar
from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()


def handler(signum, frame):
    raise Exception("Time exceeded!")

def retrieve_n100(location):
    """
       Download n100 concentrations
    """
    call(['mkdir', '-p', location])
    call(['wget', 'https://filesender.funet.fi/download.php?token=7c45b344-bea1-429e-82c2-ec8302f994eb&files_ids=100330', 
          '-O', location + '/n100.zip'])
    call(['unzip', location + '/n100.zip', '-d', location])
    call(['rm', location + '/n100.zip'])

def retrieve_cams_reanalysis(n100_location, cams_location, cities_info):
    """
       Download CAMS data for all cities we have n100 data for. CAMS oper (atmospheric model) stream
       reaches from 2003 to 2018, so those are set as limits in case n100 exceeds that.
    """
    call(['mkdir', '-p', cams_location])
    cities = pd.read_csv(cities_info)
    for index, row in cities.iterrows():
        cams_city_location = cams_location + '/' + row['city']
        call(['mkdir', '-p', cams_city_location])
        df = pd.read_csv(n100_location + '/' + row['city'] + '_N100.csv')
        # CAMS reanalysis oper stream reaches from 2003 to 2018
        yearStart = int(min(df['date'])[:4])
        if yearStart < 2003: yearStart = 2003
        yearEnd = int(max(df['date'])[:4])
        if yearEnd > 2018: yearEnd = 2018
        retrieve_cams_city(cams_city_location, row['latitude'], row['longitude'], yearStart, yearEnd)

def retrieve_cams_city(cams_city_location, latitude, longitude, yearStart, yearEnd):
    """      
       A function to demonstrate how to iterate efficiently over several years and months etc    
       for a particular CAMS Reanalysis request.     
       Change the variables below to adapt the iteration to your needs.
       You can use the variable 'target' to organise the requested data in files as you wish.
       In the example below the data are organised in files per month. (eg "cams-reanalysis_daily_200310.grb")
    """
    monthStart = 1
    monthEnd = 12
    for year in list(range(yearStart, yearEnd + 1)):
        for month in list(range(monthStart, monthEnd + 1)):
            startDate = '%04d%02d%02d' % (year, month, 1)
            numberOfDays = calendar.monthrange(year, month)[1]
            lastDate = '%04d%02d%02d' % (year, month, numberOfDays)
            target = cams_city_location + "/cams-reanalysis_daily_%04d%02d.grb" % (year, month)
            requestDates = (startDate + "/TO/" + lastDate)
            
            while True:
                # Register unix signal function handler
                signal.signal(signal.SIGALRM, handler)
                # Define retrieval timeout (20min)
                signal.alarm(1200)
                try:
                    cams_reanalysis_request(requestDates, target, latitude, longitude)
                    break
                except Exception as e:
                    # catch timeout or any other mars related errors
                    print(e)
                    print("Trying again ...")

 
def cams_reanalysis_request(requestDate, target, latitude, longitude):
    """      
        A CAMS Reanalysis request for analysis pressure level data.
        Change the keywords below to adapt it to your needs.
        (eg to add or to remove  levels, parameters, times etc)
    """
    server.retrieve({
        # Three first values needed to browse the data in the MARS catalogue
        "class": "mc", 
        "dataset": "cams_reanalysis", 
        "expver": "eac4",
        "stream": "oper", # sub-daily atmospheric model
        "type": "an", # analysis
        "date": requestDate,
        "time": "00/TO/23", # All hours containg data, 0000/0600/1200/1800
        "param": "130/210123/217027/210121/210122/217049/217016", 
        # 130: Temperature [K]
        # 210123: CO [kg(CO)/kg(air)]
        # 217027: NO [kg(NO)/kg(air)]
        # 210121: NO2 [kg(NO2)/kg(air)]
        # 210122: SO2 [kg(SO2)/kg(air)]
        # 217049: Terpenes [kg(Terpenes)/kg(air)]
        # 217016: Isoprene [kg(Isoprene)/kg(air)]
        "levtype": "ml", # Model level in CAMS reanalysis: L60
        "levelist": "60", # Highest model value possible: values 10m above ground
        "target": target,
        "grid": "1.0/1.0", # Horizontal resolution in decimal degrees
        "area": "%2.3f/%2.3f/%2.3f/%2.3f" % (latitude+1.0, longitude, latitude, longitude+1.0)    
        # Specify as N/W/S/E in geographic lat/long degrees. 
        # Southern latitudes and western longitudes must be given as negative numbers.
    })
