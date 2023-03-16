#!/opt/software/tools/python/2.7.8/bin/python

import matplotlib
#matplotlib.use('MacOSX')
import numpy as npy
import matplotlib.pylab as plt
from netCDF4 import Dataset
from netCDF4 import MFDataset

def read_sim(sim2read=None,bdys='north', s_year=None, e_year=None):
        
        ###########################################################################################################################
        ###########################################################################################################################
        ####################################        GLORYS12V1AExMercL75 ORCA12       ############################################# 
        ###########################################################################################################################
        ###########################################################################################################################

        GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon = read_sim_GLORYS12V1AExMercL75(bdys=bdys, s_year=s_year, e_year=e_year)

        LOCBDY='BERING'   ; jbegV=0 ; jbegT=0
        if bdys == 'south': 
           LOCBDY='RAPID' ; jbeg=0

        if True:
                Gyears=[]     
                c_year=s_year  ;  nleapy=0
                while c_year <= e_year :
                        ydays=365
                        if c_year == 1996  \
                        or c_year == 2000  \
                        or c_year == 2004  \
                        or c_year == 2008  \
                        or c_year == 2012  \
                        or c_year == 2016  \
                        or c_year == 2020  : 
                            print('       >>>>>>>>  ',str(c_year),' is a leap year')
                            ydays=366
                            nleapy+=1

                        t_months=(npy.arange(ydays)+0.5)/ydays   ;  cury=npy.tile(c_year,ydays)
                        
                        Gyears=npy.append(Gyears,cury+t_months)
                        c_year+=1
        else:
               Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
               c_year=s_year
               while c_year <= e_year :
                       cury=npy.tile(c_year,12)
                       Gyears=npy.append(Gyears,cury+t_months)
                       c_year+=1

        # To select the good scale foctor at v point
        cmp_data_read_dz_north=cmp_data_read_dz[:,jbegV,:].squeeze()
        cmp_ze1v_north=cmp_ze1v[jbegV,:].squeeze()
	##plt.figure(figsize=(30,15))
        ##plt.subplot(211)
        ##plt.pcolor(npy.flipud(cmp_data_read_dz_north),cmap=plt.cm.get_cmap('spectral_r'),vmin=0,vmax=30.)
        ##plt.subplot(212)
        ##for leni in set(npy.arange(cmp_data_read_dz_north.shape[1])):
        ##        plt.plot(cmp_data_read_dz_north[:,leni])
        #plt.ylim([0,20])
	#plt.grid(True)
        #plt.savefig('e3v_ps.pdf')

        GVcmp_data_read_north=GVcmp_data_read[:,:,jbegV,:].squeeze()
        #GVcmp_data_read_north[npy.where(GVcmp_data_read_north >= 1e10)]=0.e0
        #GTcmp_data_read[npy.where(GTcmp_data_read > 1e10 )]=0.e0
        #GScmp_data_read[npy.where(GScmp_data_read > 1e10 )]=0.e0
        GVcmp_data_read_north[npy.where(GVcmp_data_read_north <= -1e3)]=0.e0
        GTcmp_data_read[npy.where(GTcmp_data_read <= -1e3 )]=0.e0
        GScmp_data_read[npy.where(GScmp_data_read <= -1e3 )]=0.e0

        print('GVcmp_data_read_north shape', GVcmp_data_read_north.shape)

	# Compute the area of each vertical cell at V-point
        sec_area=npy.zeros((cmp_data_read_dz_north.shape[0],cmp_data_read_dz_north.shape[1]))
        print('sec_area shape', sec_area.shape)
        for ik in set(npy.arange(GVcmp_data_read_north.shape[1])):
            sec_area[ik,:]=cmp_data_read_dz_north[ik,:] * cmp_ze1v_north[:]

        print('Bef sec area km2:', npy.sum(sec_area)*1e-6)
        sec_area[npy.where(npy.isnan(GVcmp_data_read[0,:,jbegT,:].squeeze()))]=0.e0
        print('Aft sec area km2:', npy.sum(sec_area)*1e-6)

        # Compute mean temp/sal field at the V-point 
        ############################################
        # The calculation is done using data on the boundary (external part) and the first row (internal part)
        time_dim=(e_year-s_year+1)*365+nleapy  # Daily data
        GTdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
        GSdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
        GTdata_read_V[:,:,:] = 0.5 * (GTcmp_data_read[:,:,jbegT,:] + GTcmp_data_read[:,:,jbegT+1,:] )
        GSdata_read_V[:,:,:] = 0.5 * (GScmp_data_read[:,:,jbegT,:] + GScmp_data_read[:,:,jbegT+1,:] )
        
        # Compute net transport, heat and salt transport
        #################################################
        Gnet_volu_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
        Gnet_volu_trans=npy.zeros(  (time_dim))
        Gnet_heat_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
        Gnet_heat_trans=npy.zeros((  time_dim))  ;  Tmean=npy.zeros((  time_dim))
        Gnet_salt_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
        Gnet_salt_trans=npy.zeros((  time_dim))  ;  Smean=npy.zeros((  time_dim))

        # Compute a positive northward flux
        fac_north=-1.
        Sref=34.8
        rhocp=1023.*3900.
        if bdys == 'north' : 
                Tref=-1.9
        else:
                Tref=0.
        
        for ti in set(npy.arange(Gnet_volu_trans.shape[0])):
            for ii in set(npy.arange(GVcmp_data_read_north.shape[2])):
                for ik in set(npy.arange(GVcmp_data_read_north.shape[1])):
                    Gnet_volu_trans2D[ti,ik,ii] =  fac_north*GVcmp_data_read_north[ti,ik,ii] * cmp_data_read_dz_north[ik,ii] * cmp_ze1v_north[ii]       # [ m3 s-1 ] 
                    Gnet_heat_trans2D[ti,ik,ii] =  Gnet_volu_trans2D[ti,ik,ii] * (GTdata_read_V[ti,ik,ii]-Tref) * rhocp        # [ W ]
                    Gnet_salt_trans2D[ti,ik,ii] =  Gnet_volu_trans2D[ti,ik,ii] * (Sref-GSdata_read_V[ti,ik,ii])/Sref           # [ m3 s-1 ] 
            Gnet_volu_trans[ti] = npy.sum(Gnet_volu_trans2D[ti,:,:].squeeze())
            Gnet_heat_trans[ti] = npy.sum(Gnet_heat_trans2D[ti,:,:].squeeze())
            Gnet_salt_trans[ti] = npy.sum(Gnet_salt_trans2D[ti,:,:].squeeze())
            Tmean[ti]=npy.sum(fac_north*GTdata_read_V[ti,:,:]*sec_area[:,:])/npy.sum(sec_area)
            Smean[ti]=npy.sum(fac_north*GSdata_read_V[ti,:,:]*sec_area[:,:])/npy.sum(sec_area)


        return   Gnet_volu_trans, Gnet_heat_trans, Gnet_salt_trans, Gyears, Gnet_volu_trans2D, cmp_data_read_depth, Tmean, Smean

        
def read_sim_GLORYS12V1AExMercL75(bdys='north', s_year=None, e_year=None):
        ###########################################################################################################################
        ###########################################################################################################################
        ####################################        GLORYS12V1ExMercL75 ORCA12       ##############################################
        ###########################################################################################################################
        ###########################################################################################################################

        LOCBDY='BERING'
        if bdys == 'south': 
           LOCBDY='RAPID'

        print(LOCBDY)
        print()
        print('			READ INPUT DATA FROM  GLORYS12V1 interpolated on the CREG025.L75-NEMO420 grid')
        print 
        MYDIRGRD='./'
        # Vertical scale factor 
        file=MYDIRGRD+'CREG025.L75-NEMO420_mesh_mask_Bering_Glorys12v1_Tgt.nc'
        field = Dataset(file)
        cmp_data_read_dz = npy.squeeze(field.variables['e3v_0'])
        cmp_data_read_depth = npy.squeeze(field.variables['gdept_1d'])
        # Horizontal scale factor 
        file=MYDIRGRD+'CREG025.L75-NEMO420_mesh_mask_Bering_Glorys12v1_Tgt.nc'
        field = Dataset(file)
        cmp_ze1v = npy.squeeze(field.variables['e1v'])
        cmp_lon = npy.squeeze(field.variables['glamt'])

	# Velocities Mask 
        file=MYDIRGRD+'CREG025.L75-NEMO420_mesh_mask_Bering_Glorys12v1_Tgt.nc'
        field = Dataset(file)
        cmp_vmsk = npy.squeeze(field.variables['vmask'])
        cmp_tmsk = npy.squeeze(field.variables['tmask'])

        inDIR='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/BDYS/BERING/'
        print(inDIR)
	# Read 1 file just to get dim. size
        getsizes_ID=Dataset(inDIR+'ALL/GLORYS12V1-CREG025.L75_BERING_y1999.1d_gridT.nc')
        sizes_ID=npy.array(getsizes_ID['votemper'])
        
        GVcmp_data_read= []  ;  GTcmp_data_read= []  ;   GScmp_data_read= []
        
        Gyears=[]     ;      t_months=(npy.arange(365)+0.5)/365.
        c_year=s_year
        while c_year <= e_year :
                print("                         Read year:", c_year)
                cmp_DIR=inDIR+'/ALL/'
                fileV='GLORYS12V1-CREG025.L75_BERING_y'+str(c_year)+'.1d_gridV.nc'
                fileT='GLORYS12V1-CREG025.L75_BERING_y'+str(c_year)+'.1d_gridT.nc'
                fileS='GLORYS12V1-CREG025.L75_BERING_y'+str(c_year)+'.1d_gridS.nc'
                if c_year == s_year :
                        field = Dataset(cmp_DIR+fileV)
                        GVcmp_data_read = field.variables['vomecrty']
                        #GVcmp_data_read = field.variables['vomecrty']*cmp_vmsk
                        field = Dataset(cmp_DIR+fileT)
                        GTcmp_data_read = field.variables['votemper']
                        #GTcmp_data_read = field.variables['votemper']*cmp_tmsk
                        field = Dataset(cmp_DIR+fileS)
                        GScmp_data_read = field.variables['vosaline']
                        #GScmp_data_read = field.variables['vosaline']*cmp_tmsk
                else:
                	field = Dataset(cmp_DIR+fileV)
                	GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty'],axis=0)
                	#GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty']*cmp_vmsk,axis=0)
                	field = Dataset(cmp_DIR+fileT)
                	GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper'],axis=0)
                	#GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper']*cmp_tmsk,axis=0)
                	field = Dataset(cmp_DIR+fileS)
                	GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline'],axis=0)
                	#GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline']*cmp_tmsk,axis=0)
                
                cury=npy.tile(c_year,365)
                Gyears=npy.append(Gyears,cury+t_months)

                c_year+=1
                
        return GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon

