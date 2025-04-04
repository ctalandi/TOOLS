#!/bin/bash

import numpy as npy
import matplotlib.pylab as plt
from netCDF4 import Dataset

#####################################################################

# Choice for the resolution grid
res=1 # either 01 either 04
var='t_an' # either s_an or t_an

# Filename to read and directory 
if res == 1 :
        latxlon='1degx1deg'
else: 
   print " The choice made is not allowed"

dir='/net/5lpo154/export/drakkar-h3/drakkar/DATA/WOA2009/DATA/'+latxlon+'/CMA_DROWNED/'
dirout='/net/5lpo154/export/drakkar-h3/drakkar/DATA/WOA2009/DATA/'+latxlon+'/CMA_DROWNED_L75EX/'


if var == 's_an' :
        file='woa09_salinity_monthly_'+str(res)+'deg_s_an_CMA_drowned.nc'
        fileout='woa09_salinity_monthly_'+str(res)+'deg_s_an_CMA_drowned_Ex_L75.nc'
elif var == 't_an' :
        file='woa09_temperature_monthly_'+str(res)+'deg_t_an_CMA_drowned.nc'
        fileout='woa09_temperature_monthly_'+str(res)+'deg_t_an_CMA_drowned_Ex_L75.nc'

field = Dataset(dir+file,'r+')
readvar = npy.array(field.variables[var])

for variable in [var]:

        if variable == 't_an':
           evar='t'
           zfill=9.96921e+36
        else:
           evar='s'
           zfill=9.96921e+36
        print ' Treat variable:', variable

        for month in set(npy.arange(12)):
                if month <= 9 :
                   zmonth='0'+str(month)
                else:
                   zmonth=str(month)
                fillval=zfill
                
                # Duplicate last 2 levels with the above one
                # This step is for North Atlantic abyssal areas
                #lev_S=73 ; lev_E=74
                #readvar[:,lev_S,:,:]=readvar[:,lev_S-1,:,:]
                #readvar[:,lev_E,:,:]=readvar[:,lev_S-1,:,:]

                # Duplicate level 65 (4093.159m) on levels below 
                # to avoid proplems along the Arctic ridge which presents gap as deep as 5000m
                lev_S=64 
                ij_s=880  ; ij_e=960
                jj_s=170  ; jj_e=180
                for jk in set(npy.arange(10)+65):
                        readvar[month,jk,jj_s:jj_e,:]=readvar[month,lev_S,jj_s:jj_e,:]
                
        #plt.figure(2)
        #plt.imshow(readvar[0,50,:,:],origin='bottom')
        #plt.show()
        
        savefile=True
        if savefile:
                # Save 3D field
                print ' Save file :', fileout
                nc_f = dirout+fileout
                w_nc_fid = Dataset(nc_f, 'w', format='NETCDF4')
                w_nc_fid.description = "WOA09 field for the "+latxlon+" grid with duplicated levelswithin the Eurasian basin to avoid wrong initial state "
                w_nc_fid.createDimension('lon0', readvar.shape[3])
                w_nc_fid.createDimension('lat0', readvar.shape[2])
                w_nc_fid.createDimension('z', readvar.shape[1])
                w_nc_fid.createDimension('time_counter', None)
                #w_nc_dim = w_nc_fid.createVariable('lat0', 'f4',('lat0',))
                #w_nc_dim = w_nc_fid.createVariabl('lon0', 'f4',('lon0',))
                w_nc_var = w_nc_fid.createVariable(variable, 'f4', ('time_counter','z','lat0','lon0'))
                if variable == 't_an':
                   w_nc_var.long_name=variable
                   w_nc_var.units="degC"
                   w_nc_var._Fillvalue=fillval
                   w_nc_var.valid_range=field.variables[variable].valid_range
                   w_nc_var.coordinates=field.variables[variable].coordinates
                else:
                   w_nc_var.long_name=variable
                   w_nc_var.units="PSU"
                   w_nc_var._Fillvalue=fillval
                   w_nc_var.valid_range=field.variables[variable].valid_range
                   w_nc_var.coordinates=field.variables[variable].coordinates

                w_nc_fid.variables[variable][:,:,:,:] = readvar
                #w_nc_fid.variables['lat0'][:] = lat0
                #w_nc_fid.variables['lon0'][:] = lon0
                w_nc_fid.close()  # close the new file



