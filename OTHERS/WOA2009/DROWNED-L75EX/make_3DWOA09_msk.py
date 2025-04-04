#!/bin/bash

import numpy as npy
import PyRaf
import matplotlib.pylab as plt
from netCDF4 import Dataset

#####################################################################

# Filename to read and directory 
dir='/net/5lpo154/export/drakkar-h3/drakkar/DATA/WOA2009/DATA/1degx1deg/'
file='woa09_temperature_annual_1deg.nc'
fileout='woa09_3Dmsk_1deg.nc'



field = Dataset(dir+file)
temp = npy.squeeze(field.variables['t_an'])
lat=field.variables['lat']
lon=field.variables['lon']
fillval=field.variables['t_an'].getncattr('_FillValue')

print 'fillvalue:', fillval

lsm=npy.ones((temp.shape[0],temp.shape[1],temp.shape[2]))



print " Start to mask field"
lsm[npy.where(temp > 999999. )] = 0.
#lsm[npy.where(temp == fillval)] = 0.

#plt.figure(1)
#plt.imshow(lsm[50,:,:],origin='bottom')

#plt.figure(2)
#plt.imshow(temp[50,:,:],origin='bottom')
#
#plt.show()



# Save 3D mask field
nc_f = fileout
w_nc_fid = Dataset(nc_f, 'w', format='NETCDF4')
w_nc_fid.description = "WOA09 3D mask file for the 1degx1deg grid and built from woa09_temperature_annual_1deg.nc file"
w_nc_fid.createDimension('lon', temp.shape[2])
w_nc_fid.createDimension('lat', temp.shape[1])
w_nc_fid.createDimension('depth', temp.shape[0])
w_nc_dim = w_nc_fid.createVariable('lat', 'f4',('lat',))
w_nc_dim = w_nc_fid.createVariable('lon', 'f4',('lon',))
w_nc_var = w_nc_fid.createVariable('lsm', 'i4', ('depth','lat','lon'))
w_nc_var.setncatts({'long_name': u"land-sea mask",'units': u"bit"})
w_nc_fid.variables['lsm'][:,:,:] = lsm
w_nc_fid.variables['lat'][:] = lat
w_nc_fid.variables['lon'][:] = lon
w_nc_fid.close()  # close the new file



