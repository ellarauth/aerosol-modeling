
from subprocess import call
import calendar
from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()


def retrieve_n100(location):
    call(['mkdir', '-p', location])
    call(['wget', 'https://filesender.funet.fi/download.php?token=7c45b344-bea1-429e-82c2-ec8302f994eb&files_ids=100330', 
          '-O', location + '/n100.zip'])
    call(['unzip', location + '/n100.zip', '-d', location])
    call(['rm', location + '/n100.zip'])

def retrieve_cams_reanalysis(location):
    """      
       A function to demonstrate how to iterate efficiently over several years and months etc    
       for a particular CAMS Reanalysis request.     
       Change the variables below to adapt the iteration to your needs.
       You can use the variable 'target' to organise the requested data in files as you wish.
       In the example below the data are organised in files per month. (eg "cams-reanalysis_daily_200310.grb")
    """
    call(['mkdir', '-p', location])
    yearStart = 2003    # As of 2017/11, only 2003 CAMS reanalysis data is available.
    yearEnd = 2004
    monthStart = 1
    monthEnd = 12
    for year in list(range(yearStart, yearEnd + 1)):
        for month in list(range(monthStart, monthEnd + 1)):
            startDate = '%04d%02d%02d' % (year, month, 1)
            numberOfDays = calendar.monthrange(year, month)[1]
            lastDate = '%04d%02d%02d' % (year, month, numberOfDays)
            target = location + "/cams-reanalysis_daily_%04d%02d.grb" % (year, month)
            requestDates = (startDate + "/TO/" + lastDate)
            cams_reanalysis_request(requestDates, target)
 
def cams_reanalysis_request(requestDates, target):
    """      
        An CAMS Reanalysis request for analysis pressure level data.
        Change the keywords below to adapt it to your needs.
        (eg to add or to remove  levels, parameters, times etc)
    """
    server.retrieve({
        "class": "mc",
        "dataset": "cams_reanalysis",
        "date": requestDates,
        "decade": "2000",
        "expver": "eac4",
        "levtype": "sfc",
        "param": "167.128", # 167 = 2 metre temperature, 211127 = Total column Carbon monoxide
        "stream": "moda",
        "type": "an",
        "target": target,
        "grid": "1.0/1.0",         # Optional. The horizontal resolution in decimal degrees. If not set, the archived grid as specified in the data documentation is used.
        "area": "75/-20/10/60",    # Optional. Subset (clip) to an area. Specify as N/W/S/E in Geographic lat/long degrees. Southern latitudes and western longitudes must be
                                   # given as negative numbers. Requires "grid" to be set to a regular grid, e.g. "0.7/0.7".
    })
