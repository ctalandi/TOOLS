#!/bin/python

import numpy as npy
import PyRaf
import matplotlib.pylab as plt
from netCDF4 import Dataset

#####################################################################

# Choice for the resolution grid
res=1 #  1 only for the 1deg resolution availbable for WOA09

# Filename to read and directory 
if res == 1 :
        latxlon='1degx1deg'
else: 
   print " The choice made is not allowed"

dir='/net/5lpo154/export/drakkar-h3/drakkar/DATA/WOA2009/DATA/'+latxlon+'/MODIFIED/'
dirout='/net/5lpo154/export/drakkar-h3/drakkar/DATA/WOA2009/DATA/'+latxlon+'/COMBINED/'



for variable in ['t_an','s_an']:

        first=True   # To read depth field only once as input files

        if variable == 't_an':
           evar='temperature'
        else:
           evar='salinity'
        print ' Treat variable:', variable

        fileout='woa09_'+evar+'_monthly_'+str(res)+'deg_'+variable+'_CMA.nc'

        for month in set(npy.arange(12)+1):
                print ' Treat month:', month

                if first :
                        # Read Monthly climatology once
                        file='woa09_'+evar+'_monthly_'+str(res)+'deg_'+variable+'.nc'
                        field_mon = Dataset(dir+file,'r+')
                        readvar_mon= field_mon.variables[variable]
        
                        # Read Seasonnal climatology once
                        file_sea='woa09_'+evar+'_seasonal_'+str(res)+'deg_'+variable+'.nc'
                        field_sea = Dataset(dir+file_sea,'r+')
                        readvar_sea = field_sea.variables[variable]
                        out_var= npy.zeros((12,readvar_sea.shape[1],readvar_sea.shape[2],readvar_sea.shape[3]))
                       
                        # Fine th depthe level corresponding to 1500m
                        readdepth = field_sea.variables['depth']
                        fillval=field_sea.variables[variable].getncattr('_FillValue')
                        zlev=npy.where(readdepth[:] == 1500)[0][0]
                        print ' Find the level indice corresponding to 1500m depth which is:', zlev
                        first=False

                if month <= 3 : seas_per = 0 
                if month >  3 and month <= 6 : seas_per = 1 
                if month >  6 and month <= 9 : seas_per = 2 
                if month >  9  : seas_per = 3 

                print '                 Combine month:', month, ' with the Seasonnal period :', seas_per+1 
                print 
                print 

                # Merge Monthly fields which goes until 1500m whith annual field beyond 1500m
                out_var[month-1,0:zlev+1,:,:] = readvar_mon[month-1 ,0:zlev+1,:,:]
                out_var[month-1,zlev::  ,:,:] = readvar_sea[seas_per,zlev::  ,:,:]

        if True:
                # Save 3D field once 
                print ' Save file :', fileout
                nc_f = dirout+fileout
                w_nc_fid = Dataset(nc_f, 'w', format='NETCDF4')
                w_nc_fid.description = "WOA09 field for the "+latxlon+" grid, combine january field [0-1500]m to january-March field [1500-5500]m "
                w_nc_fid.createDimension('lon0', out_var.shape[3])
                w_nc_fid.createDimension('lat0', out_var.shape[2])
                w_nc_fid.createDimension('depth', out_var.shape[1])
                w_nc_fid.createDimension('time_counter', None)
                #w_nc_dim = w_nc_fid.createVariable('lat0', 'f4',('lat0',))
                #w_nc_dim = w_nc_fid.createVariabl('lon0', 'f4',('lon0',))
                w_nc_var = w_nc_fid.createVariable(variable, 'f4', ('time_counter','depth','lat0','lon0'))
                if variable == 't_an':
                   w_nc_var.long_name=variable
                   w_nc_var.units="degC"
                   w_nc_var._Fillvalue=fillval
                else:
                   w_nc_var.long_name=variable
                   w_nc_var.units="PSU"
                   w_nc_var._Fillvalue=fillval

                w_nc_fid.variables[variable][:,:,:,:] = out_var
                #w_nc_fid.variables['lat0'][:] = lat0
                #w_nc_fid.variables['lon0'][:] = lon0
                w_nc_fid.close()  # close the new file



