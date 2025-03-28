#!/bin/python

import numpy as np
import pandas as pd
import xarray as xr

my_year=1993
CONFIG='FREEBIORYS2V4'

# Define all areas
area_bering={'AREA':'BERING', 'lon_min' : -173., 'lon_max': -165.,'lat_min': 65., 'lat_max': 67.} 
area_subtro={'AREA':'SUBTROPGYRE', 'lon_min' : -85., 'lon_max': -5.,'lat_min': 23., 'lat_max': 30.} 
area_foldcr={'AREA':'FOLD-CREG025', 'lon_min' : -180., 'lon_max': +180.,'lat_min': 23., 'lat_max': 90.} 
area_orca25={'AREA':'ORCA025', 'lon_min' : 0., 'lon_max': 0.,'lat_min': 0., 'lat_max': 0.} 

#bgcvar_lst=['alk', 'bfe', 'bgc2D', 'caco3', 'chl', 'dchl', 'dfe', 'dic', 'doc', 'dsi', 'fe', 'goc', 'gsi', \
#           'nchl', 'nfe', 'nh4', 'no3', 'nppv', 'o2', 'par', 'ph', 'phy2', 'phyc', 'phy', 'po4', 'poc', 'sfe', 'si', 'zoo2', 'zoo']

#bgcvar_lst=['alk', 'bfe', 'caco3', 'chl', 'dchl', 'dfe', 'dic', 'doc', 'dsi', 'fe', 'goc', 'gsi', \
#           'nchl', 'nfe', 'nh4', 'no3', 'nppv', 'o2', 'par', 'phy2', 'phyc', 'phy', 'po4', 'poc', 'sfe', 'si', 'zoo2', 'zoo']

bgcvar_lst=[ 'chl']

#lst_dom=[area_bering,area_subtro]
lst_dom=[area_orca25]

# Loop on the area 
for dom_extra in lst_dom: 

    print(' The Sub-area considered is:', dom_extra['AREA'])

    # Loop on variables 
    for var in bgcvar_lst:
    
        # Read data base
        datapgn = xr.open_dataset('https://tds.mercator-ocean.fr/thredds/dodsC/freebiorys2v4-monthly-'+var)
        print()
        print('>>>>>>>  The current data read is: ', var)
        print(datapgn)
        
        if dom_extra['AREA'] == 'ORCA025' : 
            for mm in np.arange(10)+3:
            #for mm in np.arange(12)+1:
                if mm <= 9 : 
                    lmm="0"+str(mm)
                else:
                    lmm=str(mm)

                dmax=31 ;
                if mm == 4 or mm == 6 or mm == 9 or mm == 30 : dmax=30 ;
                if mm == 2 : dmax=28

                #GOOD ldate = pd.date_range(start=str(my_year)+"0101",end=str(my_year)+"0131",freq="M")
                print('start:',str(my_year)+lmm+"01", ' - end:',str(my_year)+lmm+str(dmax))
                ldate = pd.date_range(start=str(my_year)+lmm+"01",end=str(my_year)+lmm+str(dmax),freq="M") # all monday between start and end
                extra_data = datapgn.sel({'time_counter':ldate},method="nearest")
                file_out=CONFIG+'_'+dom_extra['AREA']+'_1m_y'+str(my_year)+'m'+lmm+'_'+var+'.nc'

                OUTDIR='/data0/project/drakkar/CONFIGS/ORCA025.L75/FREEBIORYS4V2/INIT/'
                extra_data.to_netcdf(OUTDIR+dom_extra['AREA']+'/'+str(my_year)+'/'+file_out)

        else: 
            geotest = (datapgn.nav_lon > dom_extra['lon_min']) & (datapgn.nav_lon < dom_extra['lon_max']) & (datapgn.nav_lat > dom_extra['lat_min']) & (datapgn.nav_lat < dom_extra['lat_max'])
            geoindex = np.argwhere(geotest.values)
            xmin = min(geoindex[:,1])
            xmax = max(geoindex[:,1])
            ymin = min(geoindex[:,0])
            ymax = max(geoindex[:,0])
            extra_data = datapgn.isel({'x':slice(xmin,xmax),'y':slice(ymin,ymax)}).sel({'time_counter':ldate},method="nearest")
            file_out=CONFIG+'_'+dom_extra['AREA']+'_1m_y'+str(my_year)+'_'+var+'.nc'
        
            OUTDIR='/data0/project/drakkar/CONFIGS/ORCA025.L75/FREEBIORYS4V2/INIT/'
            extra_data.to_netcdf(OUTDIR+dom_extra['AREA']+'/'+str(my_year)+'/'+file_out)


# Meaning of all variables 
#   alk:long_name = "Total Alkalinity" ;
#   bfe:long_name = "Iron in the big particles" ;
#   bgc2D: long_name = 
#   caco3:long_name = "Calcite" ;
#   chl:long_name = "Total Chlorophyll" ;
#   dchl:long_name = "Chlorophyll of the Diatoms" ;
#   dfe:long_name = "Iron content of the diatoms" ;
#   dic:long_name = "Dissolved Inorganic Carbon" ;
#   doc:long_name = "Dissolved Organic Carbon" ;
#   dsi:long_name = "Silicon content of the Diatoms" ;
#   fe:long_name = "Dissolved Iron" ;
#   goc:long_name = "Big Particulate Organic Carbon" ;
#   gsi:long_name = "Sinking biogenic Silica" ;
#   nchl:long_name = "Chlorophyll of the Nanophytoplankton" ;
#   nfe:long_name = "Iron content of the Nanophytoplankton" ;
#   nh4:long_name = "Ammonium" ;
#   no3:long_name = "Nitrate" ;
#   nppv:long_name = "Total Primary Production of Phyto" ;
#   o2:long_name = "Dissolved Oxygen" ;
#   par:long_name = "Photosynthetically Available Radiation" ;
#   ph:long_name = >> is a wrong variable which refers to diatoms which corresponds to variable phy2 below
#   phy2:long_name = "Diatoms"
#   phyc:long_name = "Total Phytoplankton"
#   phy:long_name = "Nanophytoplankton"
#   po4:long_name = "Phosphate"
#   poc:long_name = "Small Particulate Organic Carbon"
#   sfe:long_name = "Iron in the small particles"
#   si:long_name = "Dissolved Silicate"
#   zoo2:long_name = "Mesozooplankton" 
#   zoo:long_name = "Microzooplankton" 
#   
#   
