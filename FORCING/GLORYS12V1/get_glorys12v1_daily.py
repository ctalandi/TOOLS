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

t_year=int(sys.argv[1])
dom=sys.argv[2]

grd2D={'name':"grid2D",'varname':"sossheig"}
grdTT={'name':"gridT",'varname':"votemper"}
grdSS={'name':"gridS",'varname':"vosaline"}
grdUU={'name':"gridU",'varname':"vozocrtx"}
grdVV={'name':"gridV",'varname':"vomecrty"}
grdIC={'name':"icemod",'varname':'3 vars','varname1':"ileadfra",'varname2':"isnowthi",'varname3':"iicethic"}

list_file=[XXXgrd]
#list_file=np.append(list_file,sys.argv[3])
#list_file=[grdTT,grdSS,grdUU,grdVV]

if dom == "BER" :
      tgt_name="extGLORYS12V1-Bering"
      dirout='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/INIT/BERING/'+str(t_year)+'/'
      imin=1326
      imax=1419
      jmin=2478
      jmax=2537
      #list_file=[grd2D,grdIC]

elif dom == "SPG" :
      tgt_name="extGLORYS12V1-SubPolar"
      dirout='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/INIT/SUBPOLARGYRE/'+str(t_year)+'/'
      imin=2612
      imax=3602
      jmin=2112
      jmax=2441
      #list_file=[grd2D]

elif dom == "STG" :
      tgt_name="extGLORYS12V1-SubPolar"
      dirout='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/INIT/SUBTROPGYRE/'+str(t_year)+'/'
      imin=2470
      imax=3386
      jmin=1790
      jmax=1850
      #list_file=[grd2D]
else: 
     exit()



for typset in list_file :
         c_year=t_year
     
         print(" >>>>   The current variable treated is:",typset['varname'])

         dtaset=src_set+"-"+typset['name']

         c_month=1
         while c_month <= 12 :

            print(" >>>>   The current year is:",c_year," and month:", c_month)
            #print(" >>>>   The current year is: {02.d} and month: {02.d}".format(c_year,c_month))
            #zmm="{02.d}".format(c_month)
            if c_month <= 9:
                zmm="0"+str(c_month)
            else :
                zmm=str(c_month)
            
            # Number of days for each month
            daysinM=pd.Period(str(c_year)+"-"+zmm).days_in_month
            print("           The number of days is: ", daysinM)

            c_day=1
            while c_day <= daysinM :
                  if c_day <= 9:
                      zdd="0"+str(c_day)
                  else :
                      zdd=str(c_day)
            
                  print("                       The curent month-day is: ", zmm, "-",zdd)
                  ldate = pd.date_range(start=str(c_year)+zmm+zdd,periods=1,freq="D") 

                  dtag='y'+str(c_year)+zmm+zdd+'.1d'
                  fileout=tgt_name+"_"+dtag+"_"+typset['name']+".nc"
                  
                  if not os.path.isfile(dirout+fileout):
                      store = xr.backends.PydapDataStore.open(url+dtaset,session = session)
                      data = xr.open_dataset(store)
                      print(data) 
                      # 2 - Select area - time
                      print("get dat ok")
                      if typset['name'] == "icemod" : 
                           ext_ind= data[typset['varname1']].isel({'x':slice(imin,imax),'y':slice(jmin,jmax)}).sel({'time_counter':ldate},method="nearest")
                           ext_ind[typset['varname2']]= data[typset['varname2']].isel({'x':slice(imin,imax),'y':slice(jmin,jmax)}).sel({'time_counter':ldate},method="nearest")
                           ext_ind[typset['varname3']]= data[typset['varname3']].isel({'x':slice(imin,imax),'y':slice(jmin,jmax)}).sel({'time_counter':ldate},method="nearest")
                           print(ext_ind)
                      else:
                           ext_ind = data[typset['varname']].isel({'x':slice(imin,imax),'y':slice(jmin,jmax)}).sel({'time_counter':ldate},method="nearest")
                           print(ext_ind)

                      # 3 - Write on disk
                      print("Start to write the data ")
                      ext_ind.to_netcdf(dirout+fileout)
                      
                      print (dirout+fileout+"  done")

                  c_day+=1
            
            c_month+=1


         #dsgather=xr.open_mfdataset(dirout+tgt_name+"_"+ytag+"*.1d_"+typset['name']+".nc")
         #fileout=tgt_name+"_"+ytag+".1d_"+typset['name']+".nc"
         #dsgather.to_netcdf(dirout+fileout)
     
