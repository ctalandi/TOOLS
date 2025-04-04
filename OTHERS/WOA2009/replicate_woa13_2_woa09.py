#!/bin/python

import numpy as npy
import matplotlib.pylab as plt
from netCDF4 import Dataset
import sys

##########################################################################
# This script is dedicated to read an ASCII file from WOA13 and to save the 
# land-sea mask in a netCDF file
##########################################################################

# User choice, either s_an or t_an
fieldinit='t_an'

#########################################################################

if fieldinit == 's_an':
        tvar='salinity'
        limits=[20.,38.]
elif fieldinit == 't_an' :
        tvar='temperature'
        limits=[-2.,10.]
else:
        print ' The selectected variable name is not allowed '
        sys.exit()

dir='./'
fileout='woa09_'+tvar+'01_monthly_1deg_CMA_drownedM.nc'


# READ MASKS # 
##############

# Read mask
mask_woa09=Dataset('woa09_3Dmsk_1deg.nc').variables['lsm']
mask_woa13=Dataset('woa13_3Dmsk_01v2.nc').variables['lsm']

plt.figure('WOA09 msk')
plt.pcolormesh(mask_woa09[0,135:180,220:280])
plt.show(block=False)


plt.figure('WOA13 msk')
plt.pcolormesh(mask_woa13[0,:,:])
plt.show(block=False)

plt.figure('WOA13 msk shifted')
plt.pcolormesh(npy.roll(mask_woa13,180,axis=2)[0,:,:])
plt.show(block=False)


# READ DATA # 
#############

########################### Read WOA09 file
file='woa09_'+tvar+'01_monthly_1deg_'+fieldinit+'_CMA_drowned.nc'
fid=Dataset(dir+file)
field=fid.variables[fieldinit]
# Find the shape of arrays
nx=field.shape[3]
ny=field.shape[2]


plt.figure('WOA09 '+tvar+' init')
plt.pcolormesh(field[0,0,135:180,220:280].squeeze(),vmin=limits[0],vmax=limits[1])
plt.show(block=False)

field_surf=npy.squeeze(field[0,0,:,:])
mask_woa09_surf=npy.squeeze(mask_woa09[0,:,:])

field_msk=npy.ma.masked_where(mask_woa09_surf == 0,field_surf)
plt.figure('WOA09 '+tvar+' masked')
plt.pcolormesh(field_msk[135:180,220:280],vmin=limits[0],vmax=limits[1])
plt.show(block=False)

# Duplicate one specific point over an area
dup_val=field[0,:,160,244]
field_rep=npy.array(field).copy()
for j in npy.arange(11): 
   for i in npy.arange(9):
        field_rep[0,:,155+j,244+i]=dup_val

field_rep_surf=npy.squeeze(field_rep[0,0,:,:])
field_rep_msk=npy.ma.masked_where(mask_woa09_surf == 0,field_rep_surf)
plt.figure('WOA09 '+tvar+' changed & masked')
plt.pcolormesh(field_rep_msk[135:180,220:280],vmin=limits[0],vmax=limits[1])
plt.show(0)


########################### Read WOA13 file
#file='woa13_decav_s01_01v2_CMA_drowned.nc'
#fid=Dataset(dir+file)
#field13=fid.variables[fieldinit]
#
#plt.figure('WOA13 '+tvar+' init')
#plt.pcolormesh(field13[0,0,:,:],minval=15,maxval=39)
#plt.show(block=False)


#plt.figure()
#plt.pcolormesh(field13[0,0,:,:])
#plt.show(0)


# SAVE THE FINAL OUTPUT FIELD #
###############################
savefile=True

if savefile :
        # Simple example: temperature profile for the entire year at Darwin.
        # Open a new NetCDF file to write the data to. For format, you can choose from
        # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
        nc_f = fileout
        w_nc_fid = Dataset(nc_f, 'w', format='NETCDF4')
        w_nc_fid.description = 'WOA09 '+tvar+' field for the 1degx1deg grid, the Canadian archipelago has been filled with WOA13 data to avoid initial problems with CREG12.L75 '
        w_nc_fid.createDimension('lon0', nx)
        w_nc_fid.createDimension('lat0', ny)
        w_nc_fid.createDimension('z', 75)
        w_nc_fid.createDimension('time_counter', None)
        w_nc_var = w_nc_fid.createVariable(fieldinit, 'f8', ('time_counter','z','lat0','lon0'))
        w_nc_var.setncatts({'long_name': fid.variables[fieldinit].long_name,'units': fid.variables[fieldinit].units,'valid_range':fid.variables[fieldinit].valid_range,'coordinates':fid.variables[fieldinit].coordinates})
        w_nc_fid.variables[fieldinit][:,:,:,:] = field_rep
        w_nc_fid.close()  # close the new file
        












#
#iter=1
#f = open(dir+'test.msk', 'r')
#lat= []  ; lon = []  ;  mask = []
#for line in f:
#   print 'iter:', iter
#   if iter > 2 :
#       print 'line 1:', line
#       line = line.strip(',')
#       print 'line 2:', line
#       columns = line.split()
#       print 'columns :', columns
#       lat = npy.append(float(columns[0]),lat)
#       lon = npy.append(float(columns[1]),lon)
#       mask= npy.append(float(columns[2]),mask)
#   iter+=1
#
##f.close()
