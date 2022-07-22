import shapiro
import xarray as xr
import numpy as np
import matplotlib.pylab as plt
import glob
import os

print (shapiro.lisshapiro1d.__doc__)


# Load the data
#ds=xr.open_dataset('/data0/project/drakkar/CONFIGS/CREG12.L75/CREG12.L75-REF08-S/5d/2000/CREG12.L75-REF08_y2000m08d18.5d_gridT.nc')
#ds=xr.open_dataset('/data0/project/drakkar/CONFIGS/CREG12.L75/CREG12.L75-REF08-S/DIAGS/REL-VORT/2001/CREG12.L75-REF08_y2001m01d05.5d_IceXi.nc')

# Load mask of the CREG12 grid
dsgrd=xr.open_dataset('/data0/project/drakkar/CONFIGS/CREG12.L75/GRID/CREG12.L75-REF08_mask.nc')

# When using the fmask, need to convert the lateral condition (i.e. no-slip) from a value of 2 to 1 
#   mskm1=np.array(dsgrd['fmask'][0,0,:,:].squeeze().T)
#   msk=np.where(mskm1 == 2. , 1., mskm1 )
#   msk_condition1 = np.array(dsgrd['fmask'][0,0,:,:].squeeze())
#   msk_condition2 = np.where(msk_condition1 == 2. , 1., msk_condition1 )
msk=np.array(dsgrd['tmask'][0,0,:,:].squeeze().T)
msk_condition1 = np.array(dsgrd['tmask'][0,0,:,:].squeeze())

print('tmask 3D max:',np.max(msk))
print('tmask 3D min:',np.min(msk))

print('tmask 2D max:',np.max(msk_condition1))
print('tmask 2D min:',np.min(msk_condition1))

path_curl = '/data0/project/drakkar/CONFIGS/CREG12.L75/CREG12.L75-REF08-S/DIAGS/REL-VORT/'
#path_curl = '/data0/project/drakkar/USERS/cassianides/creg12/contribution_icurl/'
it_shap=300
index_files = [1]
#index_files = [1,4,11,12]
ylist = [2015]
#ylist = [1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015]

wnd_shap=False # To treat a 2D wind field
ice_shap=False  # To treat a 2D ice field

for i in ylist:
	for j in index_files :
		if wnd_shap :
			print('')
			print('			>>>>  Read a wind relative vorticity field ')
			print('')
			file_icurl =sorted(glob.glob('./CREG12.L75-REF08_y2015m07d05.5d_WS10.nc'), key=os.path.getmtime)
		elif ice_shap :
			print('')
			print('			>>>>  Read an Ice relative vorticity field ')
			print('')
			file_icurl =sorted(glob.glob(path_curl +str(i)+'/CREG12.L75-REF08_y'+str(i)+'m07d05.5d_IceXi.nc'), key=os.path.getmtime)
		else :
			print('')
			print('			>>>>  Read an Oce relative vorticity field ')
			print('')
			file_icurl =sorted(glob.glob(path_curl +str(i)+'/CREG12.L75-REF08_y'+str(i)+'m07d05.5d_OceXi.nc'), key=os.path.getmtime)

		#file_icurl =sorted(glob.glob(path_curl+str(i)+'/CREG12.L75-REF08_y'+str(i)+'m'+str(j).zfill(2)+'*WindVeloCurl.nc'))    
		#for l in range(0,len(file_icurl)):
		for l in range(0,1):
			print(file_icurl[l])
			ds=xr.open_dataset(file_icurl[l])
# Replace the _FIllvalue (NaN here) by zero for the process
# The transpose operation is required to pass from PYTHON to FORTRAN dimension order 
#ssh=xr.where(np.isnan(np.array(ds['ssh'][0,:,:])), 0., np.array(ds['ssh'][0,:,:].squeeze()))
			if wnd_shap or ice_shap :
 				# Set to zero all land-processors 
				ds['socurl']=xr.where(np.isnan(np.array(ds['socurl'][0,:,:])), 0., ds['socurl'])
				# Then set to zero all big <0 or >0 values due to the curl operation
                        	icurl=xr.where( (ds['socurl'] > 1.) | (ds['socurl'] < -1.), 0., np.array(ds['socurl']).squeeze())
			else :
 				# Set to zero all land-processors 
				ds['socurl']=xr.where(np.isnan(np.array(ds['socurl'][0,0,:,:])), 0., ds['socurl'])
				# Then set to zero all big <0 or >0 values due to the curl operation
                        	icurl=xr.where( (ds['socurl'][0,0,:,:] > 1.) | (ds['socurl'][0,0,:,:] < -1.), 0., np.array(ds['socurl'][0,0,:,:]).squeeze())

			# Control the min & max values B4 applying the Shapiro filter
			print('')
                        print('icurl max : ', np.max(np.array(icurl[:,:])[0]) )
                        print('icurl min : ', np.min(np.array(icurl[:,:])[0]) )

# Apply the smooth it_shap number of times 
			out=shapiro.lisshapiro1d(icurl.T,msk,it_shap)

			# Control the min & max values of the Shapiro filtering
			print('')
                        print('out max : ', np.max(out[:,:]) )
                        print('out min : ', np.min(out[:,:]) )

## Store the result in a Dataset

			ds_out=xr.Dataset()
			ds_out['icurl_smo']=(('y','x'),out.T)
			ds_out['icurl_smo']=xr.where(msk_condition1==0, np.nan, ds_out['icurl_smo'])
			if wnd_shap or ice_shap :
				ds_out['icurl_diff']=(('y','x'),ds_out['icurl_smo']-icurl[0,:,:])
			else :
				ds_out['icurl_diff']=(('y','x'),ds_out['icurl_smo']-icurl[:,:])
			ds_out
## Save the result
			if wnd_shap : 
				ds_out.to_netcdf('./CREG12.L75-REF08_y2015m07d05.5d_itpshap'+str(it_shap)+'WS10Xi.nc')
			elif ice_shap : 
				ds_out.to_netcdf('./CREG12.L75-REF08_y2015m07d05.5d_itpshap'+str(it_shap)+'IceXi.nc')
			else :
				ds_out.to_netcdf('./CREG12.L75-REF08_y2015m07d05.5d_itpshap'+str(it_shap)+'OceXi.nc')



# Plot the result and compare to the initial field
#plt.figure(figsize=(20,15))
#plt.subplot(221)
#ds['socurl'].plot(vmin=-1e-6, vmax=1e-6, cmap='Spectral_r', extend='both')
#plt.subplot(222)
#ds_out['icurl_smo'].plot(vmin=-1e-6, vmax=1e-6, cmap='Spectral_r', extend='both')
#plt.subplot(223)
#ds_out['icurl_diff'].plot(vmin=-0.1e-6, vmax=0.1e-6, extend='both')
#plt.savefig('./icurl_smooth_itShap'+str(it_shap)+'.png')

