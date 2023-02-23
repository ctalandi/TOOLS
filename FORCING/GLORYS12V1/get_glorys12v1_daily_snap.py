#!/bin/python

import os
import sys
import xarray as xr
import requests as rq
import numpy as np
import pandas as pd

# define general path
url="http://tds.mercator-ocean.fr/thredds/dodsC/"
src_set="glorys12v1-daily"
session = rq.Session()
session.auth = ("Claude.Talandier@ifremer.fr","Claude2020!!")

dom=sys.argv[1]
spec2D=False # Only for monthly file, so 2D or icemod 

if dom == "BER" :
      tgt_name="extGLORYS12V1-Bering"
      dirini='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/ADDSON/BERING/'+str(t_year)+'/'
      imin=1326
      imax=1419
      jmin=2478
      jmax=2537
      lst_tag32=['y20200404.1d_gridU.nc']
      use_lst=lst_tag32

elif dom == "SPG" :
      tgt_name="extGLORYS12V1-SubPolar"
      dirini='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/ADDSON/SUBPOLARGYRE/'+str(t_year)+'/'
      imin=2612
      imax=3602
      jmin=2112
      jmax=2441
      lst_tag8=['y20200404.1d_gridU.nc']
      use_lst=lst_tag8

elif dom == "STG" :
      tgt_name="extGLORYS12V1-SubPolar"
      dirout='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/INIT/SUBTROPGYRE/'+str(t_year)+'/'
      imin=2470
      imax=3386
      jmin=1790
      jmax=1850
else: 
     exit()

for tag in use_lst:

	print(tag)
	   
	if dom == 'BER' or spec2D : #Monthly files
		c_year=tag[1:5]
		dirout=dirini+c_year+'/'
		zmm=tag[5:7]
		tname=tag[11:16]
		if tname == 'icemo' : tname='icemod'
		if tname == 'grid2' : tname='grid2D'

		# Number of days for each month
		print("                       The curent month-day is: ", zmm)
		daysinM=pd.Period(c_year+"-"+zmm).days_in_month
		ldate = pd.date_range(start=c_year+zmm+"01",periods=daysinM,freq="D") 

		mtag='y'+c_year+zmm+'.1d'
		dtaset=src_set+"-"+tname
		fileout=tgt_name+"_"+mtag+"_"+tname+".nc"
            
	else: # Daily files
		c_year=tag[1:5]
		dirout=dirini+c_year+'/'
		zmm=tag[5:7]
		zdd=tag[7:9]
		tname=tag[13:18]
		if tname == 'icemo' : tname='icemod'
		if tname == 'grid2' : tname='grid2D'
	
		print("                       The curent month-day is: ", zmm, "-",zdd)
		ldate = pd.date_range(start=str(c_year)+zmm+zdd,periods=1,freq="D") 
		
		dtag='y'+c_year+zmm+zdd+'.1d'
		dtaset=src_set+"-"+tname
		fileout=tgt_name+"_"+dtag+"_"+tname+".nc"

	if tname == 'gridT' : 
	   tvarname='votemper'
	elif tname == 'gridS' :
	   tvarname='vosaline'
	elif tname == 'gridU' :
	   tvarname='vozocrtx'
	elif tname == 'gridV' :
	   tvarname='vomecrty'
	elif tname == 'grid2D' :
	   tvarname='sossheig'
	
	
	if not os.path.isfile(dirout+fileout):
	    store = xr.backends.PydapDataStore.open(url+dtaset,session = session)
	    data = xr.open_dataset(store)
	    print(data) 
	    # 2 - Select area - time
	    print("get dat ok")
	    if tname == "icemod" : 
	         ext_ind= data['ileadfra'].isel({'x':slice(imin,imax),'y':slice(jmin,jmax)}).sel({'time_counter':ldate},method="nearest")
	         ext_ind['isnowthi']= data['isnowthi'].isel({'x':slice(imin,imax),'y':slice(jmin,jmax)}).sel({'time_counter':ldate},method="nearest")
	         ext_ind['iicethic']= data['iicethic'].isel({'x':slice(imin,imax),'y':slice(jmin,jmax)}).sel({'time_counter':ldate},method="nearest")
	         print(ext_ind)
	    else:
	         ext_ind = data[tvarname].isel({'x':slice(imin,imax),'y':slice(jmin,jmax)}).sel({'time_counter':ldate},method="nearest")
	         print(ext_ind)
	
	    # 3 - Write on disk
	    print("Start to write the data ")
	    ext_ind.to_netcdf(dirout+fileout)
	    
	    print (dirout+fileout+"  done")

