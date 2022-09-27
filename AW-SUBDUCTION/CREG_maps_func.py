#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import sys
import numpy as npy

# Matplotlib
try:
        import matplotlib.pylab as plt
        import matplotlib as mpl
        from matplotlib import rcParams
except:
        print 'matplotlib is not available on your machine'
        print 'check python path or install this package' ; exit()

# Basemap
try:
        from mpl_toolkits.basemap import Basemap
except:
        print 'Basemap is not available on your machine'
        print 'check python path or install this package' ; exit()

# Xarray  
try:
	import xarray as xr
except:
        print 'Xarray is not available on your machine'
        print 'check python path or install this package' ; exit()


def WSC_plot(lon,lat,tab,tab_ice,ds_grd,contours,limits,myticks=None,name=None,zmy_cblab=None,zmy_cmap=None,filename='test.pdf',zvar=None,zdiff=False,zarea='L-WSC'):
	#
# Les 2 lignes suivantes posent un probleme a l'execution lie a LaTex ....
#	rcParams['text.usetex']=True
#	rcParams['text.latex.unicode']=True
	rcParams['font.family']='serif'
	plt.rcParams['contour.negative_linestyle'] = 'solid'
	zfontsize=8.
	norm = mpl.colors.Normalize(vmin=limits[0], vmax=limits[1])
	if zmy_cmap != None :
		pal = zmy_cmap
	else:
		pal = plt.cm.get_cmap('Spectral_r')
		#pal = plt.cm.get_cmap('coolwarm')
    
	zout=WSC_Bat(lon,lat,ds_grd,ztype='isol515',zarea=zarea)
	zfontsize=9.
	if zarea == 'L-WSC' : m = Basemap(width=1400000,height=1800000,lat_1=70.,lat_2=85,lon_0=10.,lat_0=77.,projection='aea',resolution='i')
	if zarea == 'S-WSC' : m = Basemap(width=1400000,height=1100000,lat_1=74.,lat_2=85,lon_0=10.,lat_0=79.,projection='aea',resolution='i')
	m.drawparallels(npy.arange(-90.,91.,1.),labels=[True,False,False,False], size=zfontsize, linewidth=0.3,alpha=0.5)
	m.drawmeridians(npy.arange(-180.,181.,5.),labels=[False,False,False,True], size=zfontsize, latmax=90.,linewidth=0.3,alpha=0.5)
	m.fillcontinents(color='grey',lake_color='white')

    	X,Y = m(lon,lat)
	C = m.contourf(X,Y,tab,contours,cmap=pal,norm=norm,extend='both')
	if zvar != None :
		if zdiff : 
			if zvar == 'Qnet' : cnt=[-20.,0.,20.]
			if zvar == 'Temp' : cnt=[-0.2,0.,0.2]
			zloc_col='g'
		else:
			if zvar == 'Qnet' : cnt=[-300.,-25.,0.]
			if zvar == 'Temp' : cnt=[2.,4.]
			zloc_col='r'
		C1= m.contour(X,Y,tab,levels=cnt, colors=zloc_col, linewidth=0.6)
		plt.clabel(C1, C1.levels, inline=True, fmt='%.0f', fontsize=zfontsize)

	C2= m.contour(X,Y,tab_ice,levels=[0.15,0.85], colors='k', linewidth=0.6)
	plt.clabel(C2, C2.levels, inline=True, fmt='%.2f', fontsize=zfontsize)

	############################################################################################################
	############################################################################################################
	moorplot=0
	if moorplot == 1 :
        	bx_ARCB={'name':'B'  ,'lon_min':-150.,'lon_max':-150.,'lat_min':78.,'lat_max':78.}
		bx_ARCM={'name':'M1' ,'lon_min': 125.,'lon_max': 125.,'lat_min':78.,'lat_max':78.}
		bx_EURA={'name':'EUR','lon_min':  60.,'lon_max':  60.,'lat_min':85.,'lat_max':85.}

		All_box=[bx_ARCB,bx_EURA]
		for box in All_box:
        		lats = [box['lat_min'],box['lat_max']]
        		lons = [box['lon_min'],box['lon_max']]
        		x,y = m(lons,lats)
        		m.scatter(x,y,1,marker='o', color='r')
        		#m.plot(x,y,linewidth=2, color='g')
	############################################################################################################
	############################################################################################################

	if zdiff : 
		zmy_fmt='%.1f'
	else:
		zmy_fmt='%.0f'
	# colorbar	
	if myticks is None:
		cbar = plt.colorbar(C,format=zmy_fmt,orientation='vertical',shrink=0.8)
	else:
		if zvar == 'votemper' or zvar == 'vosaline' or zvar == 'sivolu' :
			cbar = plt.colorbar(C,format='%.2f',orientation='vertical',shrink=0.8,drawedges=True)
		else:
			cbar = plt.colorbar(C,format='%.0f',orientation='vertical',shrink=0.8,drawedges=True)

	cbar.set_label(zmy_cblab,fontsize=zfontsize)
	cl = plt.getp(cbar.ax, 'ymajorticklabels')
	plt.setp(cl, fontsize=zfontsize)

	plt.title(name,fontsize=zfontsize)

	return m

def WSC_Bat(lon,lat,zMy_var,ztype='isol1000',zarea='L-WSC') :

	if ztype == 'isol1000' :
		vmin=1000. ; vmax=2000. 
		contours=[1000.]
		limits=[vmin,vmax]  
		myticks=[1000.]
	elif ztype == 'isol1500' :
		vmin=1500. ; vmax=2000. 
		contours=[1500.]
		limits=[vmin,vmax]  
		myticks=[1500.]
	elif ztype == 'isomonarc' :
		vmin=500. ; vmax=4000. 
		contours=[500.,2000.,4000.]
		limits=[vmin,vmax]  
		myticks=[500.,2000.,4000.]
	elif ztype == 'isol500' :
		vmin=500. ; vmax=500. 
		contours=[500.]
		limits=[vmin,vmax]  
		myticks=[500.]
	elif ztype == 'isol515' :
		vmin=500. ; vmax=500. 
		contours=[500., 1500.]
		limits=[vmin,vmax]  
		myticks=[500.,1500.]
	else:
		vmin=0. ; vmax=8000. 
		contours=[100.,500.,1000.,2000.,3000.,3500.,4000.]
		limits=[vmin,vmax] 
		myticks=[100.,500.,1000.,2000.,3000.,3500.,4000.]
	
	#
	rcParams['text.latex.unicode']=True
	plt.rcParams['contour.negative_linestyle'] = 'solid'
	#
	if zarea == 'L-WSC' : m = Basemap(width=1400000,height=1800000,lat_1=70.,lat_2=85,lon_0=10.,lat_0=77.,projection='aea',resolution='i')
	if zarea == 'S-WSC' : m = Basemap(width=1400000,height=1100000,lat_1=74.,lat_2=85,lon_0=10.,lat_0=79.,projection='aea',resolution='i')

	norm = mpl.colors.Normalize(vmin=limits[0], vmax=limits[1])
	pal = plt.cm.get_cmap('binary')
    	X,Y = m(lon,lat)

	# contour (optional)
        CS2 = m.contour(X, Y, zMy_var['Bathymetry'], linewidths=0.5,levels=contours, colors='grey', alpha=0.6)
        plt.clabel(CS2, CS2.levels, inline=True, fmt='%.0f', fontsize=9)

	return m, X, Y

