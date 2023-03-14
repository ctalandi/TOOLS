#!/opt/software/tools/python/2.7.8/bin/python

import matplotlib
#matplotlib.use('MacOSX')
import numpy as npy
import matplotlib.pylab as plt
import matplotlib as mpl
from netCDF4 import Dataset
from read_sim import read_sim_GLORYS12V1F, read_sim_GLORYS12V1A, read_sim_GLORYS12V1AEx, read_sim_GLORYS12V1AExMerc, read_sim_MJMgd16, read_sim_GLORYS2V4, read_sim_GJM189


def make_VTS_section (bdy='north' ) :

        #sel_month=2
        sel_month=8

        # Set the contours to plot
        if bdy == 'north' :
             if sel_month == 8 :
                Tvmin=-2. ; Tvmax=10. ; Tvint=0.5   # summer time
             elif sel_month == 2 :
                Tvmin=-2. ; Tvmax=2. ; Tvint=0.1   # winter time
        else:
             Tvmin=1.  ; Tvmax=27. ; Tvint=2.    # For annual mean
        
        Tcontours=npy.arange(Tvmin,Tvmax+Tvint,Tvint)
        Tlimits=[Tvmin,Tvmax]            
        Tmyticks=npy.arange(Tvmin,Tvmax+Tvint,Tvint*2.)
        Tnorm = mpl.colors.Normalize(vmin=Tlimits[0], vmax=Tlimits[1])
        
        if bdy == 'north' :
                Svmin=29.8 ; Svmax=35. ; Svint=0.2
        else:
                Svmin=34.5  ; Svmax=37.5 ; Svint=0.25
        
        Scontours=npy.arange(Svmin,Svmax+Svint,Svint)
        Slimits=[Svmin,Svmax]            
        Smyticks=npy.arange(Svmin,Svmax+Svint,Svint*2.)
        Snorm = mpl.colors.Normalize(vmin=Slimits[0], vmax=Slimits[1])
        
        if bdy == 'north' :
                Vvmin=-1.0  ; Vvmax=1.0  ; Vvint=0.1
        else:
                Vvmin=-10.  ; Vvmax=10. ; Vvint=2.  # cm s-1
                #Vvmin=-0.5  ; Vvmax=0.5 ; Vvint=0.25  # m s-1
        
        Vcontours=npy.arange(Vvmin,Vvmax+Vvint,Vvint)
        Vlimits=[Vvmin,Vvmax]            
        Vmyticks=npy.arange(Vvmin,Vvmax+Vvint,Vvint*2.5)
        Vnorm = mpl.colors.Normalize(vmin=Vlimits[0], vmax=Vlimits[1])
        
        
        plt.figure(figsize=(30,15))

        original_GLORYS12V1A=False
        if original_GLORYS12V1A:
        	# read data
        	if bdy == 'north' :
        	        syear_GLORYS12V1A=2010   ; eyear_GLORYS12V1A=2015
        	else:
        	        syear_GLORYS12V1A=2004   ; eyear_GLORYS12V1A=2014
        	GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, templon = read_sim_GLORYS12V1A(bdys=bdy, s_year=syear_GLORYS12V1A, e_year=eyear_GLORYS12V1A)
        	# transform the vector into (x,1) dimensions
        	z2dt=npy.reshape(cmp_data_read_depth,(cmp_data_read_depth.size,1))
        	# Repeat the vector z2dt GTcmp_data_read.shape[3] times along the I axis
        	zplt = npy.repeat(z2dt,GTcmp_data_read.shape[3],axis=1)
        	zlon2D=npy.tile(npy.squeeze(templon[0,:]),(cmp_data_read_dz.shape[0],1))
        	#####################################################################################################################################################################
        	#####################################################################################################################################################################
        	ax=plt.subplot(3,3,1, axisbg='darkslategray')
        	zcmap=plt.cm.get_cmap('gist_rainbow_r')
        	GTcmp_data_read=npy.ma.masked_where((GScmp_data_read >= 9e10),GTcmp_data_read)
        	if bdy == 'north' :
        	        #plt.title('\n GLORYS12V1A '+str(syear_GLORYS12V1A),size=7)
        	        plt.contourf(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.nanmean(GTcmp_data_read[:,0:25,0,:],axis=0)),Tcontours,cmap=zcmap,norm=Tnorm,vmin=Tlimits[0],vmax=Tlimits[1],extend='both')
        	        CS=plt.contour(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.nanmean(GTcmp_data_read[:,0:25,0,:],axis=0)),levels=Tmyticks,norm=Tnorm,colors='k',vmin=Tlimits[0],vmax=Tlimits[1])
        	        plt.ylim([-60., 0.])
        	        plt.xticks(fontsize=20)
        	        plt.yticks(fontsize=20)
        	        plt.ylabel(' GLORYS12V1A \n Depth (m)', size=7)
        	else:
        	        #plt.title('\n GLORYS12V1A ',size=7)
        	        plt.contourf(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GTcmp_data_read[:,:,0,:],axis=0)),Tcontours,cmap=zcmap,norm=Tnorm,vmin=Tlimits[0],vmax=Tlimits[1],extend='both')
        	        CS=plt.contour(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GTcmp_data_read[:,:,0,:],axis=0)),levels=Tmyticks,norm=Tnorm,colors='k',vmin=Tlimits[0],vmax=Tlimits[1])
        	        plt.ylim([-1500., 0.])
        	        plt.xticks(fontsize=20)
        	        plt.yticks(fontsize=20)
        	        plt.ylabel(' GLORYS12V1A \n Depth (m)', size=7)

        	plt.clabel(CS, Tmyticks, inline=True, fmt='%.1f', fontsize=20)
        	#plt.setp(ax.get_xticklabels(),visible=False)

        	ax=plt.subplot(3,3,2, axisbg='darkslategray')
        	GScmp_data_read=npy.ma.masked_where((GScmp_data_read >= 9e10),GScmp_data_read)
        	if bdy == 'north' :
        	        #plt.title('\n GLORYS12V1A '+str(syear_GLORYS12V1A),size=7)
        	        plt.contourf(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.nanmean(GScmp_data_read[:,0:25,0,:],axis=0)),Scontours,cmap=zcmap,norm=Snorm,vmin=Slimits[0],vmax=Slimits[1],extend='both')
        	        CS=plt.contour(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.nanmean(GScmp_data_read[:,0:25,0,:],axis=0)) ,levels=Smyticks,norm=Snorm,colors='k',vmin=Slimits[0],vmax=Slimits[1])
        	        plt.xticks(fontsize=20)
        	        plt.ylim([-60., 0.])
        	        plt.setp(ax.get_yticklabels(),visible=False)
        	else:
        	        #plt.title('\n GLORYS12V1A ',size=7)
        	        plt.contourf(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GScmp_data_read[:,:,0,:],axis=0)),Scontours,cmap=zcmap,norm=Snorm,vmin=Slimits[0],vmax=Slimits[1],extend='both')
        	        CS=plt.contour(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GScmp_data_read[:,:,0,:],axis=0)) ,levels=Smyticks,norm=Snorm,colors='k',vmin=Slimits[0],vmax=Slimits[1])
        	        plt.xticks(fontsize=20)
        	        plt.ylim([-1500., 0.])
        	        plt.setp(ax.get_yticklabels(),visible=False)
        	plt.clabel(CS, Smyticks, inline=True, fmt='%.1f', fontsize=20)
        	#plt.setp(ax.get_xticklabels(),visible=False)
        	
        	ax=plt.subplot(3,3,3, axisbg='darkslategray')
        	zcmap=plt.cm.get_cmap('seismic')
        	GVcmp_data_read=npy.ma.masked_where((GScmp_data_read >= 9e10 ),GVcmp_data_read)
        	if bdy == 'north' :
        	        #plt.title('\n GLORYS12V1A '+str(syear_GLORYS12V1A),size=7)
        	        plt.contourf(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.mean(GVcmp_data_read[:,0:25,0,:],axis=0)),Vcontours,cmap=zcmap,norm=Vnorm,vmin=Vlimits[0],vmax=Vlimits[1],extend='both')
        	        CS=plt.contour(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.mean(GVcmp_data_read[:,0:25,0,:],axis=0)) ,levels=Vmyticks,norm=Vnorm,colors='k',vmin=Vlimits[0],vmax=Vlimits[1])
        	        plt.xticks(fontsize=20)
        	        plt.ylim([-60., 0.])
        	        plt.setp(ax.get_yticklabels(),visible=False)
        	else:
        	        #plt.title('\n GLORYS12V1A ',size=7)
        	        plt.contourf(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(1e2*GVcmp_data_read[:,:,0,:],axis=0)),Vcontours,cmap=zcmap,norm=Vnorm,vmin=Vlimits[0],vmax=Vlimits[1],extend='both')
        	        CS=plt.contour(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(1e2*GVcmp_data_read[:,:,0,:],axis=0)) ,levels=Vmyticks,norm=Vnorm,colors='k',vmin=Vlimits[0],vmax=Vlimits[1])
        	        plt.xticks(fontsize=7)
        	        plt.ylim([-1500., 0.])
        	        plt.setp(ax.get_yticklabels(),visible=False)
        	plt.clabel(CS, Vmyticks, inline=True, fmt='%.1f', fontsize=8)
        	#plt.setp(ax.get_xticklabels(),visible=False)

        # read data
        if bdy == 'north' :
                syear_GLORYS12V1AEx=2010   ; eyear_GLORYS12V1AEx=2015
        else:
                syear_GLORYS12V1AEx=2004   ; eyear_GLORYS12V1AEx=2014
        GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, templon = read_sim_GLORYS12V1AEx(bdys=bdy, s_year=syear_GLORYS12V1AEx, e_year=eyear_GLORYS12V1AEx)
        # transform the vector into (x,1) dimensions
        z2dt=npy.reshape(cmp_data_read_depth,(cmp_data_read_depth.size,1))
        # Repeat the vector z2dt GTcmp_data_read.shape[3] times along the I axis
        zplt = npy.repeat(z2dt,GTcmp_data_read.shape[3],axis=1)
        zlon2D=npy.tile(npy.squeeze(templon[0,:]),(cmp_data_read_dz.shape[0],1))
        #####################################################################################################################################################################
        #####################################################################################################################################################################
        ax=plt.subplot(3,3,1, axisbg='darkslategray')
        zcmap=plt.cm.get_cmap('gist_rainbow_r')
        GTcmp_data_read=npy.ma.masked_where((GScmp_data_read >= 9e10),GTcmp_data_read)
        if bdy == 'north' :
                plt.title('Temperature \n mean '+str(syear_GLORYS12V1AEx)+' - '+str(eyear_GLORYS12V1AEx),size=20)
                plt.contourf(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.nanmean(GTcmp_data_read[:,0:25,0,:],axis=0)),Tcontours,cmap=zcmap,norm=Tnorm,vmin=Tlimits[0],vmax=Tlimits[1],extend='both')
                CS=plt.contour(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.nanmean(GTcmp_data_read[:,0:25,0,:],axis=0)),levels=Tmyticks,norm=Tnorm,colors='k',vmin=Tlimits[0],vmax=Tlimits[1])
                plt.ylim([-60., 0.])
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                plt.ylabel(' GLORYS12V1AEx \n Depth (m)', size=20)
        else:
                #plt.title('\n GLORYS12V1A ',size=7)
                plt.contourf(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GTcmp_data_read[:,:,0,:],axis=0)),Tcontours,cmap=zcmap,norm=Tnorm,vmin=Tlimits[0],vmax=Tlimits[1],extend='both')
                CS=plt.contour(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GTcmp_data_read[:,:,0,:],axis=0)),levels=Tmyticks,norm=Tnorm,colors='k',vmin=Tlimits[0],vmax=Tlimits[1])
                plt.ylim([-1500., 0.])
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                plt.ylabel(' GLORYS12V1AEx \n Depth (m)', size=7)

        plt.clabel(CS, Tmyticks, inline=True, fmt='%.1f', fontsize=20)
        #plt.setp(ax.get_xticklabels(),visible=False)

        ax=plt.subplot(3,3,2, axisbg='darkslategray')
        GScmp_data_read=npy.ma.masked_where((GScmp_data_read >= 9e10),GScmp_data_read)
        if bdy == 'north' :
                plt.title('Salinity \n mean '+str(syear_GLORYS12V1AEx)+' - '+str(eyear_GLORYS12V1AEx),size=20)
                plt.contourf(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.nanmean(GScmp_data_read[:,0:25,0,:],axis=0)),Scontours,cmap=zcmap,norm=Snorm,vmin=Slimits[0],vmax=Slimits[1],extend='both')
                CS=plt.contour(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.nanmean(GScmp_data_read[:,0:25,0,:],axis=0)) ,levels=Smyticks,norm=Snorm,colors='k',vmin=Slimits[0],vmax=Slimits[1])
                plt.xticks(fontsize=20)
                plt.ylim([-60., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        else:
                #plt.title('\n GLORYS12V1A ',size=7)
                plt.contourf(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GScmp_data_read[:,:,0,:],axis=0)),Scontours,cmap=zcmap,norm=Snorm,vmin=Slimits[0],vmax=Slimits[1],extend='both')
                CS=plt.contour(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GScmp_data_read[:,:,0,:],axis=0)) ,levels=Smyticks,norm=Snorm,colors='k',vmin=Slimits[0],vmax=Slimits[1])
                plt.xticks(fontsize=20)
                plt.ylim([-1500., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        plt.clabel(CS, Smyticks, inline=True, fmt='%.1f', fontsize=20)
        #plt.setp(ax.get_xticklabels(),visible=False)
        
        ax=plt.subplot(3,3,3, axisbg='darkslategray')
        zcmap=plt.cm.get_cmap('seismic')
        GVcmp_data_read=npy.ma.masked_where((GScmp_data_read >= 9e10 ),GVcmp_data_read)
        if bdy == 'north' :
                plt.title('Velocity \n mean '+str(syear_GLORYS12V1AEx)+' - '+str(eyear_GLORYS12V1AEx),size=20)
                plt.contourf(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.mean(GVcmp_data_read[:,0:25,0,:],axis=0)),Vcontours,cmap=zcmap,norm=Vnorm,vmin=Vlimits[0],vmax=Vlimits[1],extend='both')
                CS=plt.contour(zlon2D[0:25,:],npy.flipud(-1.*zplt[0:25,:]),npy.flipud(npy.mean(GVcmp_data_read[:,0:25,0,:],axis=0)) ,levels=Vmyticks,norm=Vnorm,colors='k',vmin=Vlimits[0],vmax=Vlimits[1])
                plt.xticks(fontsize=20)
                plt.ylim([-60., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        else:
                #plt.title('\n GLORYS12V1A ',size=7)
                plt.contourf(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(1e2*GVcmp_data_read[:,:,0,:],axis=0)),Vcontours,cmap=zcmap,norm=Vnorm,vmin=Vlimits[0],vmax=Vlimits[1],extend='both')
                CS=plt.contour(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(1e2*GVcmp_data_read[:,:,0,:],axis=0)) ,levels=Vmyticks,norm=Vnorm,colors='k',vmin=Vlimits[0],vmax=Vlimits[1])
                plt.xticks(fontsize=7)
                plt.ylim([-1500., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        plt.clabel(CS, Vmyticks, inline=True, fmt='%.1f', fontsize=20)
        #plt.setp(ax.get_xticklabels(),visible=False)


        # read data
        if bdy == 'north' :
                syear_MJMgd16=2010   ; eyear_MJMgd16=2015
        else:
                syear_MJMgd16=2004   ; eyear_MJMgd16=2014
        GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, templon = read_sim_MJMgd16(bdys=bdy, s_year=syear_MJMgd16, e_year=eyear_MJMgd16)
        # transform the vector into (x,1) dimensions
        print(cmp_data_read_depth.shape)
        z2dt=npy.reshape(cmp_data_read_depth,(cmp_data_read_depth.size,1))
        #####################################################################################################################################################################
        #####################################################################################################################################################################

        ax=plt.subplot(3,3,4, axisbg='darkslategray')
        zcmap=plt.cm.get_cmap('gist_rainbow_r')
        jbegS=39 # At South of the domain
        ibeg=55 ;  eend=860  # At South of the domain remove Mexico Gulf and Africa coast
        jbeg=25 # At Bering
        is_beg=13 ; ie_beg=40 
        #is_beg=13 ; ie_beg=37 
        # Repeat the vector z2dt GTcmp_data_read.shape[3] times along the I axis
        print(GTcmp_data_read.shape)
        print(templon.shape)
        zplt = npy.repeat(z2dt,GTcmp_data_read.shape[3],axis=1)
        if bdy == 'north' :
                zlon2D=npy.tile(npy.squeeze(templon[jbeg,:]),(cmp_data_read_dz.shape[0],1))
        else:
                zlon2D=npy.tile(npy.squeeze(templon[jbegS,:]),(cmp_data_read_dz.shape[0],1))
        print('zlon2D.shape', zlon2D.shape)
        if sel_month == 8 : 
           strmonth='July'
        elif sel_month == 2 :
           strmonth='March'
        GTcmp_data_read=npy.ma.masked_where((GScmp_data_read == 0),GTcmp_data_read)
        if bdy == 'north' :
                #plt.title(' \n MJMgd16 '+str(syear_MJMgd16),size=7)
                plt.contourf(  zlon2D[0:25,is_beg:ie_beg],npy.flipud(-1.*zplt[0:25,is_beg:ie_beg]),npy.flipud(npy.nanmean(GTcmp_data_read[:,0:25,jbeg,is_beg:ie_beg],axis=0)),Tcontours,cmap=zcmap,norm=Tnorm,vmin=Tlimits[0],vmax=Tlimits[1],extend='both')
                CS=plt.contour(zlon2D[0:25,is_beg:ie_beg],npy.flipud(-1.*zplt[0:25,is_beg:ie_beg]),npy.flipud(npy.nanmean(GTcmp_data_read[:,0:25,jbeg,is_beg:ie_beg],axis=0)),levels=Tmyticks,norm=Tnorm,colors='k',vmin=Tlimits[0],vmax=Tlimits[1])
                plt.ylim([-60., 0.])
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                plt.ylabel(' MJMgd16 \n Depth (m)', size=20)
        else:
                #plt.title('\n MJMgd16 ',size=7)
                plt.contourf(  zlon2D[:,ibeg:eend],npy.flipud(-1.*zplt[:,ibeg:eend]),npy.flipud(npy.mean(GTcmp_data_read[:,:,jbegS,ibeg:eend],axis=0)),Tcontours,cmap=zcmap,norm=Tnorm,vmin=Tlimits[0],vmax=Tlimits[1],extend='both')
                CS=plt.contour(zlon2D[:,ibeg:eend],npy.flipud(-1.*zplt[:,ibeg:eend]),npy.flipud(npy.mean(GTcmp_data_read[:,:,jbegS,ibeg:eend],axis=0)),levels=Tmyticks,norm=Tnorm,colors='k',vmin=Tlimits[0],vmax=Tlimits[1])
                plt.ylim([-1500., 0.])
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                plt.ylabel(' MJMgd16 \n Depth (m)', size=20)

        plt.clabel(CS, Tmyticks, inline=True, fmt='%.1f', fontsize=20)
        #plt.setp(ax.get_xticklabels(),visible=False)

        ax=plt.subplot(3,3,5, axisbg='darkslategray')
        GScmp_data_read=npy.ma.masked_where((GScmp_data_read == 0),GScmp_data_read)
        if bdy == 'north' :
                #plt.title(' \n MJMgd16 '+str(syear_MJMgd16),size=7)
                plt.contourf(  zlon2D[0:25,is_beg:ie_beg],npy.flipud(-1.*zplt[0:25,is_beg:ie_beg]),npy.flipud(npy.nanmean(GScmp_data_read[:,0:25,jbeg,is_beg:ie_beg],axis=0)),Scontours,cmap=zcmap,norm=Snorm,vmin=Slimits[0],vmax=Slimits[1],extend='both')
                CS=plt.contour(zlon2D[0:25,is_beg:ie_beg],npy.flipud(-1.*zplt[0:25,is_beg:ie_beg]),npy.flipud(npy.nanmean(GScmp_data_read[:,0:25,jbeg,is_beg:ie_beg],axis=0)) ,levels=Smyticks,norm=Snorm,colors='k',vmin=Slimits[0],vmax=Slimits[1])
                plt.xticks(fontsize=20)
                plt.ylim([-60., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        else:
                #plt.title(' \n MJMgd16 ',size=7)
                plt.contourf(  zlon2D[:,ibeg:eend],npy.flipud(-1.*zplt[:,ibeg:eend]),npy.flipud(npy.mean(GScmp_data_read[:,:,jbegS,ibeg:eend],axis=0)),Scontours,cmap=zcmap,norm=Snorm,vmin=Slimits[0],vmax=Slimits[1],extend='both')
                CS=plt.contour(zlon2D[:,ibeg:eend],npy.flipud(-1.*zplt[:,ibeg:eend]),npy.flipud(npy.mean(GScmp_data_read[:,:,jbegS,ibeg:eend],axis=0)) ,levels=Smyticks,norm=Snorm,colors='k',vmin=Slimits[0],vmax=Slimits[1])
                plt.xticks(fontsize=20)
                plt.ylim([-1500., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        plt.clabel(CS, Smyticks, inline=True, fmt='%.1f', fontsize=20)
        #plt.setp(ax.get_xticklabels(),visible=False)
        
        ax=plt.subplot(3,3,6, axisbg='darkslategray')
        zcmap=plt.cm.get_cmap('seismic')
        GVcmp_data_read=npy.ma.masked_where((GScmp_data_read == 0 ),GVcmp_data_read)
        if bdy == 'north' :
                #plt.title(' \n MJMgd16 '+str(syear_MJMgd16),size=7)
                plt.contourf(  zlon2D[0:25,is_beg:ie_beg],npy.flipud(-1.*zplt[0:25,is_beg:ie_beg]),npy.flipud(npy.nanmean(GVcmp_data_read[:,0:25,jbeg,is_beg:ie_beg],axis=0)),Vcontours,cmap=zcmap,norm=Vnorm,vmin=Vlimits[0],vmax=Vlimits[1],extend='both')
                CS=plt.contour(zlon2D[0:25,is_beg:ie_beg],npy.flipud(-1.*zplt[0:25,is_beg:ie_beg]),npy.flipud(npy.nanmean(GVcmp_data_read[:,0:25,jbeg,is_beg:ie_beg],axis=0)) ,levels=Vmyticks,norm=Vnorm,colors='k',vmin=Vlimits[0],vmax=Vlimits[1])
                plt.xticks(fontsize=20)
                plt.ylim([-60., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        else:
                #plt.title(' \n MJMgd16 ',size=7)
                plt.contourf(  zlon2D[:,ibeg:eend],npy.flipud(-1.*zplt[:,ibeg:eend]),npy.flipud(npy.mean(1e2*GVcmp_data_read[:,:,jbegS,ibeg:eend],axis=0)),Vcontours,cmap=zcmap,norm=Vnorm,vmin=Vlimits[0],vmax=Vlimits[1],extend='both')
                CS=plt.contour(zlon2D[:,ibeg:eend],npy.flipud(-1.*zplt[:,ibeg:eend]),npy.flipud(npy.mean(1e2*GVcmp_data_read[:,:,jbegS,ibeg:eend],axis=0)) ,levels=Vmyticks,norm=Vnorm,colors='k',vmin=Vlimits[0],vmax=Vlimits[1])
                plt.xticks(fontsize=7)
                plt.ylim([-1500., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        plt.clabel(CS, Vmyticks, inline=True, fmt='%.1f', fontsize=20, linewidth=0.7)
        #plt.setp(ax.get_xticklabels(),visible=False)
        

        # read data
        if bdy == 'north' :
                syear_GLORYS12V1AExMerc=2016   ; eyear_GLORYS12V1AExMerc=2018
        else:
                syear_GLORYS12V1AExMerc=2004   ; eyear_GLORYS12V1AExMerc=2014
        GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, templon = read_sim_GLORYS12V1AExMerc(bdys=bdy, s_year=syear_GLORYS12V1AExMerc, e_year=eyear_GLORYS12V1AExMerc)
        # transform the vector into (x,1) dimensions
        z2dt=npy.reshape(cmp_data_read_depth,(cmp_data_read_depth.size,1))
        # Repeat the vector z2dt GTcmp_data_read.shape[3] times along the I axis
        zplt = npy.repeat(z2dt,GTcmp_data_read.shape[3],axis=1)
        zlon2D=npy.tile(npy.squeeze(templon[0,:]),(cmp_data_read_dz.shape[0],1))
        #####################################################################################################################################################################
        #####################################################################################################################################################################
        ax=plt.subplot(3,3,7, axisbg='darkslategray')
        zcmap=plt.cm.get_cmap('gist_rainbow_r')
        GTcmp_data_read=npy.ma.masked_where((GScmp_data_read >= 9e10),GTcmp_data_read)
        if bdy == 'north' :
                plt.title('\n mean '+str(syear_GLORYS12V1AExMerc)+' - '+str(eyear_GLORYS12V1AExMerc),size=20)
                plt.contourf(zlon2D[0:25,8:35],npy.flipud(-1.*zplt[0:25,8:35]),npy.flipud(npy.nanmean(GTcmp_data_read[:,0:25,0,8:35],axis=0)),Tcontours,cmap=zcmap,norm=Tnorm,vmin=Tlimits[0],vmax=Tlimits[1],extend='both')
                CS=plt.contour(zlon2D[0:25,8:35],npy.flipud(-1.*zplt[0:25,8:35]),npy.flipud(npy.nanmean(GTcmp_data_read[:,0:25,0,8:35],axis=0)),levels=Tmyticks,norm=Tnorm,colors='k',vmin=Tlimits[0],vmax=Tlimits[1])
                plt.ylim([-60., 0.])
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                plt.ylabel(' GLORYS12V1AExMerc \n Depth (m)', size=20)
        else:
                #plt.title('\n GLORYS12V1A ',size=7)
                plt.contourf(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GTcmp_data_read[:,:,0,:],axis=0)),Tcontours,cmap=zcmap,norm=Tnorm,vmin=Tlimits[0],vmax=Tlimits[1],extend='both')
                CS=plt.contour(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GTcmp_data_read[:,:,0,:],axis=0)),levels=Tmyticks,norm=Tnorm,colors='k',vmin=Tlimits[0],vmax=Tlimits[1])
                plt.ylim([-1500., 0.])
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                plt.ylabel(' GLORYS12V1AExMerc \n Depth (m)', size=7)

        plt.clabel(CS, Tmyticks, inline=True, fmt='%.1f', fontsize=20)
        #plt.setp(ax.get_xticklabels(),visible=False)

        ax=plt.subplot(3,3,8, axisbg='darkslategray')
        GScmp_data_read=npy.ma.masked_where((GScmp_data_read >= 9e10),GScmp_data_read)
        if bdy == 'north' :
                plt.title('\n mean '+str(syear_GLORYS12V1AExMerc)+' - '+str(eyear_GLORYS12V1AExMerc),size=20)
                plt.contourf(zlon2D[0:25,8:35],npy.flipud(-1.*zplt[0:25,8:35]),npy.flipud(npy.nanmean(GScmp_data_read[:,0:25,0,8:35],axis=0)),Scontours,cmap=zcmap,norm=Snorm,vmin=Slimits[0],vmax=Slimits[1],extend='both')
                CS=plt.contour(zlon2D[0:25,8:35],npy.flipud(-1.*zplt[0:25,8:35]),npy.flipud(npy.nanmean(GScmp_data_read[:,0:25,0,8:35],axis=0)) ,levels=Smyticks,norm=Snorm,colors='k',vmin=Slimits[0],vmax=Slimits[1])
                plt.xticks(fontsize=20)
                plt.ylim([-60., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        else:
                #plt.title('\n GLORYS12V1A ',size=7)
                plt.contourf(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GScmp_data_read[:,:,0,:],axis=0)),Scontours,cmap=zcmap,norm=Snorm,vmin=Slimits[0],vmax=Slimits[1],extend='both')
                CS=plt.contour(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(GScmp_data_read[:,:,0,:],axis=0)) ,levels=Smyticks,norm=Snorm,colors='k',vmin=Slimits[0],vmax=Slimits[1])
                plt.xticks(fontsize=20)
                plt.ylim([-1500., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        plt.clabel(CS, Smyticks, inline=True, fmt='%.1f', fontsize=20)
        #plt.setp(ax.get_xticklabels(),visible=False)
        
        ax=plt.subplot(3,3,9, axisbg='darkslategray')
        zcmap=plt.cm.get_cmap('seismic')
        GVcmp_data_read=npy.ma.masked_where((GScmp_data_read >= 9e10 ),GVcmp_data_read)
        if bdy == 'north' :
                plt.title('\n mean '+str(syear_GLORYS12V1AExMerc)+' - '+str(eyear_GLORYS12V1AExMerc),size=20)
                plt.contourf(zlon2D[0:25,8:35],npy.flipud(-1.*zplt[0:25,8:35]),npy.flipud(npy.mean(GVcmp_data_read[:,0:25,0,8:35],axis=0)),Vcontours,cmap=zcmap,norm=Vnorm,vmin=Vlimits[0],vmax=Vlimits[1],extend='both')
                CS=plt.contour(zlon2D[0:25,8:35],npy.flipud(-1.*zplt[0:25,8:35]),npy.flipud(npy.mean(GVcmp_data_read[:,0:25,0,8:35],axis=0)) ,levels=Vmyticks,norm=Vnorm,colors='k',vmin=Vlimits[0],vmax=Vlimits[1])
                plt.xticks(fontsize=20)
                plt.ylim([-60., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        else:
                #plt.title('\n GLORYS12V1A ',size=7)
                plt.contourf(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(1e2*GVcmp_data_read[:,:,0,:],axis=0)),Vcontours,cmap=zcmap,norm=Vnorm,vmin=Vlimits[0],vmax=Vlimits[1],extend='both')
                CS=plt.contour(zlon2D[:,:],npy.flipud(-1.*zplt[:,:]),npy.flipud(npy.mean(1e2*GVcmp_data_read[:,:,0,:],axis=0)) ,levels=Vmyticks,norm=Vnorm,colors='k',vmin=Vlimits[0],vmax=Vlimits[1])
                plt.xticks(fontsize=7)
                plt.ylim([-1500., 0.])
                plt.setp(ax.get_yticklabels(),visible=False)
        plt.clabel(CS, Vmyticks, inline=True, fmt='%.1f', fontsize=20)
        #plt.setp(ax.get_xticklabels(),visible=False)


        #####################################################################################################################################################################
        #####################################################################################################################################################################
        #####################################################################################################################################################################
        #####################################################################################################################################################################
        #####################################################################################################################################################################
        #####################################################################################################################################################################
        #####################################################################################################################################################################
        #####################################################################################################################################################################
        # Plot the WOA09 Temp & salinity along both sections

        TS_woa09=False
        if TS_woa09 :
	        zcmap=plt.cm.get_cmap('gist_rainbow_r')
	        if bdy == 'north' :
	                jbeg=1799 # At Bering
	                is_beg=619 ; ie_beg=646 
	                #is_beg=621 ; ie_beg=646 
	                file=Dataset('CREG12.L75-REF02_y1979m0'+str(sel_month+1)+'.5d_gridT.nc')
	        else:
	                jbeg=1 # At South
	                is_beg=160 ; ie_beg=949 
	                file=Dataset('CREG12.L75-REF02_init_gridT.nc')
	
	        woa09T = npy.array(npy.squeeze(file.variables['votemper']))
	        woa09S = npy.array(npy.squeeze(file.variables['vosaline']))
	        z_woa09 = npy.array(npy.squeeze(file.variables['deptht']))
	        lon_woa09 = npy.array(npy.squeeze(file.variables['nav_lon']))
	        file=Dataset('CREG12.L75-REF01_mask.nc')
	        tmask = npy.array(npy.squeeze(file.variables['tmask']))
	        print(woa09T.shape)
	
	
	
	        # transform the vector into (x,1) dimensions
	        z2dt=npy.reshape(z_woa09,(z_woa09.size,1))
	        print('z_woa09.size', z_woa09.size)
	        print(z2dt.shape)
	        # Repeat the vector z2dt GTcmp_data_read.shape[3] times along the I axis
	        zplt = npy.repeat(z2dt,woa09T.shape[2],axis=1)
	        zlon2D=npy.tile(npy.squeeze(lon_woa09[jbeg,:]),(z_woa09.shape[0],1))
	
	        ax=plt.subplot(6,3,16, axisbg='darkslategray')
	        woa09T=npy.ma.masked_where((tmask == 0),woa09T)
	        if bdy == 'north' :
	                plt.contourf(  npy.fliplr(zlon2D[0:25,is_beg:ie_beg]),npy.fliplr(-1.*zplt[0:25,is_beg:ie_beg]),npy.fliplr(woa09T[0:25,jbeg,is_beg:ie_beg]),Tcontours,cmap=zcmap,norm=Tnorm,vmin=Tlimits[0],vmax=Tlimits[1],extend='both')
	                CS=plt.contour(npy.fliplr(zlon2D[0:25,is_beg:ie_beg]),npy.fliplr(-1.*zplt[0:25,is_beg:ie_beg]),npy.fliplr(woa09T[0:25,jbeg,is_beg:ie_beg]),levels=Tmyticks,norm=Tnorm,colors='k',vmin=Tlimits[0],vmax=Tlimits[1])
	                plt.ylim([-60., 0.])
	                plt.xticks(fontsize=7)
	                plt.yticks(fontsize=7)
	                plt.ylabel(' WOA09 \n Depth (m)', size=7)
	        else:
	                plt.contourf(  zlon2D[:,is_beg:ie_beg],-1.*zplt[:,is_beg:ie_beg],woa09T[:,jbeg,is_beg:ie_beg],Tcontours,cmap=zcmap,norm=Tnorm,vmin=Tlimits[0],vmax=Tlimits[1],extend='both')
	                CS=plt.contour(zlon2D[:,is_beg:ie_beg],-1.*zplt[:,is_beg:ie_beg],woa09T[:,jbeg,is_beg:ie_beg],levels=Tmyticks,norm=Tnorm,colors='k',vmin=Tlimits[0],vmax=Tlimits[1])
	                plt.ylim([-1500., 0.])
	                plt.xticks(fontsize=7)
	                plt.yticks(fontsize=7)
	                plt.ylabel(' WOA09 \n Depth (m)', size=7)
	
	        plt.clabel(CS, Tmyticks, inline=True, fmt='%.1f', fontsize=8)
	
	        ax=plt.subplot(6,3,17, axisbg='darkslategray')
	        woa09S=npy.ma.masked_where((tmask == 0),woa09S)
	        if bdy == 'north' :
	                plt.contourf(  npy.fliplr(zlon2D[0:25,is_beg:ie_beg]),npy.fliplr(-1.*zplt[0:25,is_beg:ie_beg]),npy.fliplr(woa09S[0:25,jbeg,is_beg:ie_beg]),Scontours,cmap=zcmap,norm=Snorm,vmin=Slimits[0],vmax=Slimits[1],extend='both')
	                CS=plt.contour(npy.fliplr(zlon2D[0:25,is_beg:ie_beg]),npy.fliplr(-1.*zplt[0:25,is_beg:ie_beg]),npy.fliplr(woa09S[0:25,jbeg,is_beg:ie_beg]),levels=Smyticks,norm=Snorm,colors='k',vmin=Slimits[0],vmax=Slimits[1])
	                plt.xticks(fontsize=7)
	                plt.ylim([-60., 0.])
	                plt.setp(ax.get_yticklabels(),visible=False)
	        else:
	                plt.contourf(  zlon2D[:,is_beg:ie_beg],-1.*zplt[:,is_beg:ie_beg],woa09S[:,jbeg,is_beg:ie_beg],Scontours,cmap=zcmap,norm=Snorm,vmin=Slimits[0],vmax=Slimits[1],extend='both')
	                CS=plt.contour(zlon2D[:,is_beg:ie_beg],-1.*zplt[:,is_beg:ie_beg],woa09S[:,jbeg,is_beg:ie_beg],levels=Smyticks,norm=Snorm,colors='k',vmin=Slimits[0],vmax=Slimits[1])
	                plt.ylim([-1500., 0.])
	                plt.xticks(fontsize=7)
	                plt.setp(ax.get_yticklabels(),visible=False)
	        plt.clabel(CS, Smyticks, inline=True, fmt='%.1f', fontsize=8)
        





        
        if bdy == 'north' : 
                dosavefig=True
                if dosavefig : plt.savefig('./FIGURES/Bering_Res112_SEC_VTS_y'+str(syear_GLORYS12V1AEx)+str(eyear_GLORYS12V1AExMerc)+'.pdf')
                dosavefig=False
        else:
                dosavefig=True
                if dosavefig : plt.savefig('./FIGURES/RAPID_Res112_SEC_VTS_y'+str(syear_GLORYS12V1AEx)+str(eyear_GLORYS12V1AExMerc)+'.pdf')
                dosavefig=False

        plt.show(1)
        

        return

