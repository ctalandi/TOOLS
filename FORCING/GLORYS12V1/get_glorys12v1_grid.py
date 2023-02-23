#!/bin/python

import os
import sys
import xarray as xr
import requests as rq
import numpy as np
import pandas as pd

# define general path
url="http://tds.mercator-ocean.fr/thredds/dodsC/psy4v3r1/global-analysis-forecast-phy-001-024-pgnstatics/"
src_set="glorys12v1"
session = rq.Session()
session.auth = ("Claude.Talandier@ifremer.fr","Claude2020!!")

dom=sys.argv[1]

grdmsk={'name':"PSY4V3R1_mask",'name_out':"mask"}
grdzgr={'name':"PSY4V3R1_mesh_zgr",'name_out':"mesh_zgr"}
grdhgr={'name':"PSY4V3R1_mesh_hgr",'name_out':"mesh_hgr"}

list_file=[grdmsk,grdzgr,grdhgr]

if dom == "BER" :
      tgt_name="extGLORYS12V1-Bering"
      dirout='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/BERING/GRID/'
      imin=1326
      imax=1419
      jmin=2478
      jmax=2537

elif dom == "SPG" :
      tgt_name="extGLORYS12V1-SubPolar"
      dirout='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/SUBPOLARGYRE/GRID/'
      imin=2612
      imax=3602
      jmin=2112
      jmax=2441

elif dom == "STG" :
      tgt_name="extGLORYS12V1-SubPolar"
      dirout='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/INIT/SUBTROPGYRE/GRID/'
      imin=2470
      imax=3386
      jmin=1790
      jmax=1850
      #list_file=[grd2D]
else: 
     exit()



for typset in list_file :
     
         #print(" >>>>   The current variable treated is:",typset['varname'])

         
         dtaset=typset['name']+".nc"
         fileout=tgt_name+"_"+typset['name_out']+".nc"
         print(fileout)
         print(url+dtaset)
         
         if not os.path.isfile(dirout+fileout):
             store = xr.backends.PydapDataStore.open(url+dtaset,session = session)
             data = xr.open_dataset(store)
             print(data) 
             # 2 - Select area
             print("get dat ok")
             ext_ind = data.isel({'x':slice(imin,imax),'y':slice(jmin,jmax)})
             print(ext_ind)

             ext_ind.to_netcdf(dirout+fileout)
             
             print (dirout+fileout+"  done")
         
