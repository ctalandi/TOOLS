#!/bin/python

# Python script for geting data from the Mercator opendap
#  revised version of the example provided by Mercator.
#  This script can be used for Initial condition and for BDY condition 
#  However, note that this is just an extraction of GLORY12v1, with 50 vertical levels.
#  Extracted data will be processed ahead for producing suitable BDY/Initial conditions

import os
import xarray as xr
import requests as rq
import numpy as np

# define general path
url="http://tds.mercator-ocean.fr/thredds/dodsC/"
src_set="glorys12v1-daily"
dirout='./EXTRACTION/'
session = rq.Session()
session.auth = ("Claude.Talandier@ifremer.fr",'QkPm4CDsLg')

s_year=2000
e_year=2000

# isel method is use to select data by index
# GRID 2D
# 1 - open dataset

Bering_area=({'area_name:','Bering', 'lon_min:', -173., 'lon_max:', -164., 'lat_min:', 65. , 'lat_max:', 67. })
Subpol_area=({'area_name:','SpgNor', 'lon_min:',  -70., 'lon_max:',   14., 'lat_min:', 46. , 'lat_max:', 60. })
BOX=[Bering_area,Subpol_area]
# Bering Box
#lon_min=-173.
#lon_max=-164.
#lat_min=65.
#lat_max=67.
# The box above give the following indices
#xmin=1326 xmax=1419 ymin=2478 ymax=2537

# Subpolar gyre Box
lon_min=-70.
lon_max=14.
lat_min=46.
lat_max=60.
# The box above give the following indices
# xmin=2612 xmax=3602 ymin=2112 ymax=2441             

c_year=s_year

typset="gridT"
dtaset=src_set+"-"+typset
    
print ("url+dtaset:", url+dtaset , " session:", session)
store = xr.backends.PydapDataStore.open(url+dtaset,session = session)
datapgn = xr.open_dataset(store)

geotest = (datapgn.nav_lon > lon_min) & (datapgn.nav_lon < lon_max) & (datapgn.nav_lat > lat_min) & (datapgn.nav_lat < lat_max)
geoindex = np.argwhere(geotest.values)
xmin = min(geoindex[:,1])
xmax = max(geoindex[:,1])
ymin = min(geoindex[:,0])
ymax = max(geoindex[:,0])

print(xmin,ymin,xmin,xmax)
