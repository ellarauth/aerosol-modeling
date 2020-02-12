nn#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
   
server = ECMWFDataServer()
server.retrieve({
    "class": "mc",
    "dataset": "cams_reanalysis",
    "expver": "eac4",
    "stream": "oper",
    "type": "an",
    "levtype": "sfc",
    "param": "167.128",
    "date": "2003-12-01",
    "time": "00:00:00/03:00:00",
    "grid": "1.0/1.0",
    "area": "75/-20/10/60",
    "format": "netcdf",
    "target": "test.nc"
 })
