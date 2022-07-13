import shapiro
import xarray as xr
import numpy as np
import matplotlib.pylab as plt

print shapiro.lisshapiro1d.__doc__

# Load the data
ds=xr.open_dataset('/data0/project/drakkar/CONFIGS/CREG12.L75/CREG12.L75-REF08-S/5d/2000/CREG12.L75-REF08_y2000m08d18.5d_gridT.nc')

# Load mask of the CREG12 grid
dsgrd=xr.open_dataset('/data0/project/drakkar/CONFIGS/CREG12.L75/GRID/CREG12.L75-REF08_mask.nc')

# Replace the _FIllvalue (NaN here) by zero for the process
# The transpose operation is required to pass from PYTHON to FORTRAN dimension order 
ssh=xr.where(np.isnan(np.array(ds['ssh'][0,:,:])), 0., np.array(ds['ssh'][0,:,:].squeeze()))
msk=np.array(dsgrd['tmask'][0,0,:,:].squeeze().T)

# Apply the smooth it_shap number of times 
it_shap=200
out=shapiro.lisshapiro1d(ssh.T,msk,it_shap)

# Store the result in a Dataset
ds_out=xr.Dataset()
ds_out['ssh_smo']=(('y','x'),out.T)
ds_out['ssh_diff']=(('y','x'),out.T-ssh)
ds_out
# Save the result
ds_out.to_netcdf('./ssh_smooth_Shapiro'+str(it_shap)+'.nc')

# Plot the result and compare to the initial field
plt.figure(figsize=(20,15))
plt.subplot(221)
ds['ssh'].plot(vmin=-1., vmax=1., cmap='Spectral_r', extend='both')
plt.subplot(222)
ds_out['ssh_smo'].plot(vmin=-1., vmax=1., cmap='Spectral_r', extend='both')
plt.subplot(223)
ds_out['ssh_diff'].plot(vmin=-0.1, vmax=0.1, extend='both')
plt.savefig('./ssh_smooth_itShap'+str(it_shap)+'.png',dpi=150)

