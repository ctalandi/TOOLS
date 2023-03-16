#!/opt/software/tools/python/2.7.8/bin/python

import matplotlib
#matplotlib.use('MacOSX')
import numpy as npy
import matplotlib.pylab as plt
from netCDF4 import Dataset
from netCDF4 import MFDataset

def read_sim(sim2read=None,bdys='north', s_year=None, e_year=None):

        
        if sim2read == 'GLORYS12V1-ORCA12':
                ###########################################################################################################################
                ###########################################################################################################################
                ####################################        GLORYS12V1 ORCA12       ######################################################### 
                ###########################################################################################################################
                ###########################################################################################################################

                GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon = read_sim_GLORYS12V1A(bdys=bdys, s_year=s_year, e_year=e_year)

                LOCBDY='BERING'   ; jbeg=0
                if bdys == 'south': 
                   LOCBDY='RAPID' ; jbeg=0

                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)
                        c_year+=1

                # To select the good scale foctor at v point
                cmp_data_read_dz_north=cmp_data_read_dz[:,jbeg,:].squeeze()
                cmp_ze1v_north=cmp_ze1v[jbeg,:].squeeze()
                #plt.subplot(211)
                #plt.imshow(cmp_data_read_dz_north,cmap=plt.cm.get_cmap('cool'))
                #plt.subplot(212)
                #for leni in set(npy.arange(cmp_data_read_dz_north.shape[1])):
                #        plt.plot(cmp_data_read_dz_north[:,leni])
                #plt.ylim([0,20])
                #plt.savefig('e3v_ps.pdf')

                GVcmp_data_read_north=GVcmp_data_read[:,:,jbeg,:].squeeze()
                GVcmp_data_read_north[npy.where(GVcmp_data_read_north >= 1e10)]=0.e0
                #GVcmp_data_read_north[npy.where(npy.isnan(GVcmp_data_read_north))]=0.e0
		#GTcmp_data_read[npy.where(npy.isnan(GTcmp_data_read))]=0.e0
		#GScmp_data_read[npy.where(npy.isnan(GScmp_data_read))]=0.e0
                print('GVcmp_data_read_north shape', GVcmp_data_read_north.shape)
		
		# Compute the area of each vertical cell at V-point
                sec_area=npy.zeros((cmp_data_read_dz_north.shape[0],cmp_data_read_dz_north.shape[1]))
                for ik in set(npy.arange(GVcmp_data_read_north.shape[1])):
                       sec_area[ik,:]=cmp_data_read_dz_north[ik,:] * cmp_ze1v_north[:]

                sec_area[npy.where(GVcmp_data_read[0,:,jbeg,:].squeeze() >= 1e10)]=0.e0

                # Compute mean temp/sal field at the V-point 
                ############################################
                # The calculation is done using data on the boundary (external part) and the first row (internal part)
                time_dim=(e_year-s_year+1)*12
                GTdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                GSdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                GTdata_read_V[:,:,:] = 0.5 * (GTcmp_data_read[:,:,jbeg,:] + GTcmp_data_read[:,:,jbeg+1,:] )
                GSdata_read_V[:,:,:] = 0.5 * (GScmp_data_read[:,:,jbeg,:] + GScmp_data_read[:,:,jbeg+1,:] )
                
                # Compute net transport, heat and salt transport
                #################################################
                Gnet_volu_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_volu_trans=npy.zeros(  (time_dim)) 
                Gnet_heat_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_heat_trans=npy.zeros((  time_dim)) ;  Tmean=npy.zeros((  time_dim))
                Gnet_salt_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_salt_trans=npy.zeros((  time_dim)) ;  Smean=npy.zeros((  time_dim))

                # Compute a positive northward flux
                fac_north=+1.
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


        elif sim2read == 'GLORYS12V1AEx-ORCA12':
                ###########################################################################################################################
                ###########################################################################################################################
                ####################################        GLORYS12V1AEx ORCA12       #################################################### 
                ###########################################################################################################################
                ###########################################################################################################################

                GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon = read_sim_GLORYS12V1AEx(bdys=bdys, s_year=s_year, e_year=e_year)

                LOCBDY='BERING'   ; jbeg=0
                if bdys == 'south': 
                   LOCBDY='RAPID' ; jbeg=0

                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)
                        c_year+=1

                # To select the good scale foctor at v point
                cmp_data_read_dz_north=cmp_data_read_dz[:,jbeg,:].squeeze()
                cmp_ze1v_north=cmp_ze1v[jbeg,:].squeeze()
		### plt.figure(figsize=(30,15))
                ### plt.subplot(211)
                ### plt.pcolor(npy.flipud(cmp_data_read_dz_north),cmap=plt.cm.get_cmap('spectral_r'),vmin=0,vmax=30.)
                ### plt.subplot(212)
                ### for leni in set(npy.arange(cmp_data_read_dz_north.shape[1])):
                ###         plt.plot(cmp_data_read_dz_north[:,leni])
                ### plt.ylim([0,20])
		### plt.grid(True)
                ### plt.savefig('e3v_ps.pdf')

                GVcmp_data_read_north=GVcmp_data_read[:,:,jbeg,:].squeeze()
                GVcmp_data_read_north[npy.where(GVcmp_data_read_north >= 1e10)]=0.e0
                GTcmp_data_read[npy.where(GTcmp_data_read > 1e10 )]=0.e0
                GScmp_data_read[npy.where(GScmp_data_read > 1e10 )]=0.e0

                #GVcmp_data_read_north[npy.where(npy.isnan(GVcmp_data_read_north))]=0.e0
		#GTcmp_data_read[npy.where(npy.isnan(GTcmp_data_read))]=0.e0
		#GScmp_data_read[npy.where(npy.isnan(GScmp_data_read))]=0.e0

                print('GVcmp_data_read_north shape', GVcmp_data_read_north.shape)

                # Compute the area of each vertical cell at V-point
                sec_area=npy.zeros((cmp_data_read_dz_north.shape[0],cmp_data_read_dz_north.shape[1]))
                print('sec_area shape', sec_area.shape)
                for ik in set(npy.arange(GVcmp_data_read_north.shape[1])):
                    sec_area[ik,:]=cmp_data_read_dz_north[ik,:] * cmp_ze1v_north[:]

                print('Bef sec area km2:', npy.sum(sec_area)*1e-6)
                #sec_area[npy.where(GVcmp_data_read_north >= 0 )]=0.e0
                #sec_area[npy.where(npy.isnan(GVcmp_data_read[0,:,jbeg,:].squeeze()))]=0.e0
                print('Aft sec area km2:', npy.sum(sec_area)*1e-6)

                # Compute mean temp/sal field at the V-point 
                ############################################
                # The calculation is done using data on the boundary (external part) and the first row (internal part)
                time_dim=(e_year-s_year+1)*12
                GTdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                GSdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                GTdata_read_V[:,:,:] = 0.5 * (GTcmp_data_read[:,:,jbeg,:] + GTcmp_data_read[:,:,jbeg+1,:] )
                GSdata_read_V[:,:,:] = 0.5 * (GScmp_data_read[:,:,jbeg,:] + GScmp_data_read[:,:,jbeg+1,:] )
                
                # Compute net transport, heat and salt transport
                #################################################
                Gnet_volu_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_volu_trans=npy.zeros(  (time_dim))
                Gnet_heat_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_heat_trans=npy.zeros((  time_dim))  ;  Tmean=npy.zeros((  time_dim))
                Gnet_salt_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_salt_trans=npy.zeros((  time_dim))  ;  Smean=npy.zeros((  time_dim))

                # Compute a positive northward flux
                fac_north=+1.
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

        elif sim2read == 'GLORYS12V1AExMerc-ORCA12':
                ###########################################################################################################################
                ###########################################################################################################################
                ####################################        GLORYS12V1AExMerc ORCA12       ################################################ 
                ###########################################################################################################################
                ###########################################################################################################################

                GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon = read_sim_GLORYS12V1AExMerc(bdys=bdys, s_year=s_year, e_year=e_year)

                LOCBDY='BERING'   ; jbeg=0
                if bdys == 'south': 
                   LOCBDY='RAPID' ; jbeg=0

                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)
                        c_year+=1

                # To select the good scale foctor at v point
                cmp_data_read_dz_north=cmp_data_read_dz[:,jbeg,:].squeeze()
                cmp_ze1v_north=cmp_ze1v[jbeg,:].squeeze()
		##plt.figure(figsize=(30,15))
                ##plt.subplot(211)
                ##plt.pcolor(npy.flipud(cmp_data_read_dz_north),cmap=plt.cm.get_cmap('spectral_r'),vmin=0,vmax=30.)
                ##plt.subplot(212)
                ##for leni in set(npy.arange(cmp_data_read_dz_north.shape[1])):
                ##        plt.plot(cmp_data_read_dz_north[:,leni])
                #plt.ylim([0,20])
		#plt.grid(True)
                #plt.savefig('e3v_ps.pdf')

                GVcmp_data_read_north=GVcmp_data_read[:,:,jbeg,:].squeeze()
                GVcmp_data_read_north[npy.where(GVcmp_data_read_north >= 1e10)]=0.e0
                GTcmp_data_read[npy.where(GTcmp_data_read > 1e10 )]=0.e0
                GScmp_data_read[npy.where(GScmp_data_read > 1e10 )]=0.e0

                print('GVcmp_data_read_north shape', GVcmp_data_read_north.shape)

                # Compute the area of each vertical cell at V-point
                sec_area=npy.zeros((cmp_data_read_dz_north.shape[0],cmp_data_read_dz_north.shape[1]))
                print('sec_area shape', sec_area.shape)
                for ik in set(npy.arange(GVcmp_data_read_north.shape[1])):
                    sec_area[ik,:]=cmp_data_read_dz_north[ik,:] * cmp_ze1v_north[:]

                print('Bef sec area km2:', npy.sum(sec_area)*1e-6)
                sec_area[npy.where(npy.isnan(GVcmp_data_read[0,:,jbeg,:].squeeze()))]=0.e0
                print('Aft sec area km2:', npy.sum(sec_area)*1e-6)

                # Compute mean temp/sal field at the V-point 
                ############################################
                # The calculation is done using data on the boundary (external part) and the first row (internal part)
                time_dim=(e_year-s_year+1)*12
                GTdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                GSdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                GTdata_read_V[:,:,:] = 0.5 * (GTcmp_data_read[:,:,jbeg,:] + GTcmp_data_read[:,:,jbeg+1,:] )
                GSdata_read_V[:,:,:] = 0.5 * (GScmp_data_read[:,:,jbeg,:] + GScmp_data_read[:,:,jbeg+1,:] )
                
                # Compute net transport, heat and salt transport
                #################################################
                Gnet_volu_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_volu_trans=npy.zeros(  (time_dim))
                Gnet_heat_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_heat_trans=npy.zeros((  time_dim))  ;  Tmean=npy.zeros((  time_dim))
                Gnet_salt_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_salt_trans=npy.zeros((  time_dim))  ;  Smean=npy.zeros((  time_dim))

                # Compute a positive northward flux
                fac_north=+1.
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

        elif sim2read == 'GLORYS12V1AExMercL75-ORCA12':
                ###########################################################################################################################
                ###########################################################################################################################
                ####################################        GLORYS12V1AExMercL75 ORCA12       ############################################# 
                ###########################################################################################################################
                ###########################################################################################################################

                GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon = read_sim_GLORYS12V1AExMercL75(bdys=bdys, s_year=s_year, e_year=e_year)

                LOCBDY='BERING'   ; jbegV=0 ; jbegT=0 # The position of the raw to read 
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

        
        elif sim2read == 'EORCA12.L75-MJMgd16' :
                ###########################################################################################################################
                ###########################################################################################################################
                ###########################          EORCA12.L75-MJMgd16             ######################################################
                ###########################################################################################################################
                ###########################################################################################################################

                GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon = read_sim_MJMgd16(bdys=bdys, s_year=s_year, e_year=e_year)

                LOCBDY='BERING'   ; jbeg=25   ; ibeg=5     ;   iend=47  ;  xdim=iend-ibeg

                if bdys == 'south': 
                        LOCBDY='RAPID' ; jbeg=35   ; ibeg=56 ; iend=860  ;  xdim=iend-ibeg

                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)
                        c_year+=1

                cmp_data_read_dz_north=cmp_data_read_dz[:,jbeg,ibeg:iend].squeeze()
                print(cmp_data_read_dz_north.shape)
                cmp_ze1v_north=cmp_ze1v[jbeg,ibeg:iend].squeeze()

                GVcmp_data_read_north=GVcmp_data_read[:,:,jbeg,ibeg:iend].squeeze()
                GVcmp_data_read_north[npy.where(GVcmp_data_read_north >= 1e10)]=0.e0

		# Compute the area of each vertical cell at V-point
                sec_area=npy.zeros((cmp_data_read_dz_north.shape[0],cmp_data_read_dz_north.shape[1]))
                for ik in set(npy.arange(GVcmp_data_read_north.shape[1])):
                    sec_area[ik,:]=cmp_data_read_dz_north[ik,:] * cmp_ze1v_north[:]

                sec_area[npy.where(GVcmp_data_read[0,:,jbeg,ibeg:iend].squeeze() >= 1e10)]=0.e0

                # Compute mean temp/sal field at the V-point 
                ############################################
                # The calculation is done using data on the boundary (external part) and the first row (internal part)
                time_dim=(e_year-s_year+1)*12
                GTdata_read_V= npy.zeros((time_dim,75,xdim))
                GSdata_read_V= npy.zeros((time_dim,75,xdim))
                GTdata_read_V[:,:,:] = 0.5 * (GTcmp_data_read[:,:,jbeg,ibeg:iend] + GTcmp_data_read[:,:,jbeg+1,ibeg:iend] )
                GSdata_read_V[:,:,:] = 0.5 * (GScmp_data_read[:,:,jbeg,ibeg:iend] + GScmp_data_read[:,:,jbeg+1,ibeg:iend] )
                
                # Compute net transport, heat and salt transport
                #################################################
                Gnet_volu_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],GVcmp_data_read_north.shape[2]))
                Gnet_volu_trans=npy.zeros(  (time_dim))
                Gnet_heat_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],GVcmp_data_read_north.shape[2]))
                Gnet_heat_trans=npy.zeros((  time_dim))  ;  Tmean=npy.zeros((  time_dim))
                Gnet_salt_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],GVcmp_data_read_north.shape[2]))
                Gnet_salt_trans=npy.zeros((  time_dim))  ;  Smean=npy.zeros((  time_dim))

                # Compute a positive northward flux
                fac_north=+1.
                Sref=34.8       
                rhocp=1023.*3900.
                if bdys == 'north' : 
                        Tref=-1.9
                else:
                        Tref=0.
                
                for ti in set(npy.arange(Gnet_volu_trans.shape[0])):
                    for ii in set(npy.arange(GVcmp_data_read_north.shape[2])):
                        for ik in set(npy.arange(75)):
                            Gnet_volu_trans2D[ti,ik,ii] =  fac_north*GVcmp_data_read_north[ti,ik,ii] * cmp_data_read_dz_north[ik,ii] * cmp_ze1v_north[ii]       # [ m3 s-1 ] 
                            Gnet_heat_trans2D[ti,ik,ii] =  Gnet_volu_trans2D[ti,ik,ii] * (GTdata_read_V[ti,ik,ii]-Tref) * rhocp        # [ W ]
                            Gnet_salt_trans2D[ti,ik,ii] =  Gnet_volu_trans2D[ti,ik,ii] * (Sref-GSdata_read_V[ti,ik,ii])/Sref           # [ m3 s-1 ] 
                    Gnet_volu_trans[ti] = npy.sum(Gnet_volu_trans2D[ti,:,:].squeeze())
                    Gnet_heat_trans[ti] = npy.sum(Gnet_heat_trans2D[ti,:,:].squeeze())
                    Gnet_salt_trans[ti] = npy.sum(Gnet_salt_trans2D[ti,:,:].squeeze())
                    Tmean[ti]=npy.sum(fac_north*GTdata_read_V[ti,:,:]*sec_area[:,:])/npy.sum(sec_area)
                    Smean[ti]=npy.sum(fac_north*GSdata_read_V[ti,:,:]*sec_area[:,:])/npy.sum(sec_area)

        elif sim2read == 'GJM2020-ORCA12' :
                ###########################################################################################################################
                ###########################################################################################################################
                ###########################          eORCA12.L75-GJM2020             ######################################################
                ###########################################################################################################################
                ###########################################################################################################################

                GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon = read_sim_GJM2020(bdys=bdys, s_year=s_year, e_year=e_year)

                LOCBDY='BERING'   ; jbeg=20   ; ibeg=24     ;   iend=62  ;  xdim=iend-ibeg

                if bdys == 'south': 
                        LOCBDY='RAPID' ; jbeg=35   ; ibeg=56 ; iend=860  ;  xdim=iend-ibeg

                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)
                        c_year+=1

                cmp_data_read_dz_north=cmp_data_read_dz[:,jbeg,ibeg:iend].squeeze()
                print(cmp_data_read_dz_north.shape)
                cmp_ze1v_north=cmp_ze1v[jbeg,ibeg:iend].squeeze()

                GVcmp_data_read_north=GVcmp_data_read[:,:,jbeg,ibeg:iend].squeeze()
                GVcmp_data_read_north[npy.where(GVcmp_data_read_north >= 1e10)]=0.e0

		# Compute the area of each vertical cell at V-point
                sec_area=npy.zeros((cmp_data_read_dz_north.shape[0],cmp_data_read_dz_north.shape[1]))
                for ik in set(npy.arange(GVcmp_data_read_north.shape[1])):
                    sec_area[ik,:]=cmp_data_read_dz_north[ik,:] * cmp_ze1v_north[:]

                sec_area[npy.where(GVcmp_data_read[0,:,jbeg,ibeg:iend].squeeze() >= 1e10)]=0.e0

                # Compute mean temp/sal field at the V-point 
                ############################################
                # The calculation is done using data on the boundary (external part) and the first row (internal part)
                time_dim=(e_year-s_year+1)*12
                GTdata_read_V= npy.zeros((time_dim,75,xdim))
                GSdata_read_V= npy.zeros((time_dim,75,xdim))
                GTdata_read_V[:,:,:] = 0.5 * (GTcmp_data_read[:,:,jbeg,ibeg:iend] + GTcmp_data_read[:,:,jbeg+1,ibeg:iend] )
                GSdata_read_V[:,:,:] = 0.5 * (GScmp_data_read[:,:,jbeg,ibeg:iend] + GScmp_data_read[:,:,jbeg+1,ibeg:iend] )
                
                # Compute net transport, heat and salt transport
                #################################################
                Gnet_volu_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],GVcmp_data_read_north.shape[2]))
                Gnet_volu_trans=npy.zeros(  (time_dim))
                Gnet_heat_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],GVcmp_data_read_north.shape[2]))
                Gnet_heat_trans=npy.zeros((  time_dim))  ;  Tmean=npy.zeros((  time_dim))
                Gnet_salt_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],GVcmp_data_read_north.shape[2]))
                Gnet_salt_trans=npy.zeros((  time_dim))  ;  Smean=npy.zeros((  time_dim))

                # Compute a positive northward flux
                fac_north=+1.
                Sref=34.8       
                rhocp=1023.*3900.
                if bdys == 'north' : 
                        Tref=-1.9
                else:
                        Tref=0.
                
                for ti in set(npy.arange(Gnet_volu_trans.shape[0])):
                    for ii in set(npy.arange(GVcmp_data_read_north.shape[2])):
                        for ik in set(npy.arange(75)):
                            Gnet_volu_trans2D[ti,ik,ii] =  fac_north*GVcmp_data_read_north[ti,ik,ii] * cmp_data_read_dz_north[ik,ii] * cmp_ze1v_north[ii]       # [ m3 s-1 ] 
                            Gnet_heat_trans2D[ti,ik,ii] =  Gnet_volu_trans2D[ti,ik,ii] * (GTdata_read_V[ti,ik,ii]-Tref) * rhocp        # [ W ]
                            Gnet_salt_trans2D[ti,ik,ii] =  Gnet_volu_trans2D[ti,ik,ii] * (Sref-GSdata_read_V[ti,ik,ii])/Sref           # [ m3 s-1 ] 
                    Gnet_volu_trans[ti] = npy.sum(Gnet_volu_trans2D[ti,:,:].squeeze())
                    Gnet_heat_trans[ti] = npy.sum(Gnet_heat_trans2D[ti,:,:].squeeze())
                    Gnet_salt_trans[ti] = npy.sum(Gnet_salt_trans2D[ti,:,:].squeeze())
                    Tmean[ti]=npy.sum(fac_north*GTdata_read_V[ti,:,:]*sec_area[:,:])/npy.sum(sec_area)
                    Smean[ti]=npy.sum(fac_north*GSdata_read_V[ti,:,:]*sec_area[:,:])/npy.sum(sec_area)


        elif sim2read == 'GLORYS2V4' :
                ###########################################################################################################################
                ###########################################################################################################################
                ###########################                 GLORYS2V4                ######################################################
                ###########################################################################################################################
                ###########################################################################################################################
                
                GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon = read_sim_GLORYS2V4(bdys=bdys, s_year=s_year, e_year=e_year)
                
                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)
                        c_year+=1

                cmp_data_read_dz_north=cmp_data_read_dz[:,0,:].squeeze()
                cmp_ze1v_north=cmp_ze1v[0,:].squeeze()

                GVcmp_data_read_north=GVcmp_data_read[:,:,0,:].squeeze()
                GVcmp_data_read_north[npy.where(GVcmp_data_read_north >= 1e10)]=0.e0

		# Compute the area of each vertical cell at V-point
                sec_area=npy.zeros((cmp_data_read_dz_north.shape[0],cmp_data_read_dz_north.shape[1]))
                for ik in set(npy.arange(GVcmp_data_read_north.shape[1])):
                    sec_area[ik,:]=cmp_data_read_dz_north[ik,:] * cmp_ze1v_north[:]

                sec_area[npy.where(GVcmp_data_read[0,:,0,:].squeeze() >= 1e10)]=0.e0


                # Compute mean temp/sal field at the V-point 
                ############################################
                # The calculation is done using data on the boundary (external part) and the first row (internal part)
                time_dim=(e_year-s_year+1)*12
                if bdys == 'north' :
                        GTdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                        GSdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                        GTdata_read_V[:,:,:] = 0.5 * (GTcmp_data_read[:,:,0,:] + GTcmp_data_read[:,:,1,:] )
                        GSdata_read_V[:,:,:] = 0.5 * (GScmp_data_read[:,:,0,:] + GScmp_data_read[:,:,1,:] )
                
                # Compute net transport, heat and salt transport
                #################################################
                Gnet_volu_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_volu_trans=npy.zeros(  (time_dim))
                Gnet_heat_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_heat_trans=npy.zeros((  time_dim))  ;  Tmean=npy.zeros((  time_dim))
                Gnet_salt_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_salt_trans=npy.zeros((  time_dim))  ;  Smean=npy.zeros((  time_dim))

                # Compute a positive northward flux
                fac_north=+1.
                Sref=34.8    ;   Tref=-1.9
                rhocp=1023.*3900.
                
                for ti in set(npy.arange(Gnet_volu_trans.shape[0])):
                    for ii in set(npy.arange(GVcmp_data_read_north.shape[2])):
                        for ik in set(npy.arange(75)):
                            Gnet_volu_trans2D[ti,ik,ii] =  fac_north*GVcmp_data_read_north[ti,ik,ii] * cmp_data_read_dz_north[ik,ii] * cmp_ze1v_north[ii]       # [ m3 s-1 ] 
                            if bdys == 'north' :
                            	Gnet_heat_trans2D[ti,ik,ii] =  Gnet_volu_trans2D[ti,ik,ii] * (GTdata_read_V[ti,ik,ii]-Tref) * rhocp        # [ W ]
                            	Gnet_salt_trans2D[ti,ik,ii] =  Gnet_volu_trans2D[ti,ik,ii] * (Sref-GSdata_read_V[ti,ik,ii])/Sref           # [ m3 s-1 ] 
                    Gnet_volu_trans[ti] = npy.sum(Gnet_volu_trans2D[ti,:,:].squeeze())
                    if bdys == 'north' :
                    	Gnet_heat_trans[ti] = npy.sum(Gnet_heat_trans2D[ti,:,:].squeeze())
                    	Gnet_salt_trans[ti] = npy.sum(Gnet_salt_trans2D[ti,:,:].squeeze())
                    Tmean[ti]=npy.sum(fac_north*GTdata_read_V[ti,:,:]*sec_area[:,:])/npy.sum(sec_area)
                    Smean[ti]=npy.sum(fac_north*GSdata_read_V[ti,:,:]*sec_area[:,:])/npy.sum(sec_area)


        elif sim2read == 'ORCA025.L75-GJM189' :
                ###########################################################################################################################
                ###########################################################################################################################
                ###########################         ORCA025.L75-GJM189               ######################################################
                ###########################################################################################################################
                ###########################################################################################################################
                
                GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon = read_sim_GJM189(bdys=bdys, s_year=s_year, e_year=e_year)
                
                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)
                        c_year+=1

                cmp_data_read_dz_north=cmp_data_read_dz[:,0,:].squeeze()
                cmp_ze1v_north=cmp_ze1v[0,:].squeeze()

                GVcmp_data_read_north=GVcmp_data_read[:,:,0,:].squeeze()
                GVcmp_data_read_north[npy.where(GVcmp_data_read_north >= 1e10)]=0.e0

		# Compute the area of each vertical cell at V-point
                sec_area=npy.zeros((cmp_data_read_dz_north.shape[0],cmp_data_read_dz_north.shape[1]))
                for ik in set(npy.arange(GVcmp_data_read_north.shape[1])):
                    sec_area[ik,:]=cmp_data_read_dz_north[ik,:] * cmp_ze1v_north[:]

                sec_area[npy.where(GVcmp_data_read[0,:,0,:].squeeze() >= 1e10)]=0.e0


                # Compute mean temp/sal field at the V-point 
                ############################################
                # The calculation is done using data on the boundary (external part) and the first row (internal part)
                time_dim=(e_year-s_year+1)*12
                if bdys == 'north' :
                	GTdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                	GSdata_read_V= npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                	GTdata_read_V[:,:,:] = 0.5 * (GTcmp_data_read[:,:,0,:] + GTcmp_data_read[:,:,1,:] )
                	GSdata_read_V[:,:,:] = 0.5 * (GScmp_data_read[:,:,0,:] + GScmp_data_read[:,:,1,:] )
                
                # Compute net transport, heat and salt transport
                #################################################
                Gnet_volu_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_volu_trans=npy.zeros(  (time_dim))
                Gnet_heat_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_heat_trans=npy.zeros((  time_dim))  ;  Tmean=npy.zeros((  time_dim))
                Gnet_salt_trans2D=npy.zeros((time_dim,sizes_ID.shape[1],sizes_ID.shape[3]))
                Gnet_salt_trans=npy.zeros((  time_dim))  ;  Smean=npy.zeros((  time_dim))

                # Compute a positive northward flux
                if bdys == 'north' : 
                        fac_north=-1.  # The negative sign is because the field is ready for CREG grid (i.e. east-west flipped and U/V velocities sign changed)
                else:
                        fac_north=+1.  
                Sref=34.8    ;   Tref=-1.9
                rhocp=1023.*3900.
                
                for ti in set(npy.arange(Gnet_volu_trans.shape[0])):
                    for ii in set(npy.arange(GVcmp_data_read_north.shape[2])):
                        for ik in set(npy.arange(75)):
                            Gnet_volu_trans2D[ti,ik,ii] =  fac_north*GVcmp_data_read_north[ti,ik,ii] * cmp_data_read_dz_north[ik,ii] * cmp_ze1v_north[ii]       # [ m3 s-1 ] 
                            if bdys == 'north' :
                            	Gnet_heat_trans2D[ti,ik,ii] =  Gnet_volu_trans2D[ti,ik,ii] * (GTdata_read_V[ti,ik,ii]-Tref) * rhocp        # [ W ]
                            	Gnet_salt_trans2D[ti,ik,ii] =  Gnet_volu_trans2D[ti,ik,ii] * (Sref-GSdata_read_V[ti,ik,ii])/Sref           # [ m3 s-1 ] 
                    Gnet_volu_trans[ti] = npy.sum(Gnet_volu_trans2D[ti,:,:].squeeze())
                    if bdys == 'north' :
                    	Gnet_heat_trans[ti] = npy.sum(Gnet_heat_trans2D[ti,:,:].squeeze())
                    	Gnet_salt_trans[ti] = npy.sum(Gnet_salt_trans2D[ti,:,:].squeeze())
                    Tmean[ti]=npy.sum(fac_north*GTdata_read_V[ti,:,:]*sec_area[:,:])/npy.sum(sec_area)
                    Smean[ti]=npy.sum(fac_north*GSdata_read_V[ti,:,:]*sec_area[:,:])/npy.sum(sec_area)


        return   Gnet_volu_trans, Gnet_heat_trans, Gnet_salt_trans, Gyears, Gnet_volu_trans2D, cmp_data_read_depth, Tmean, Smean
        

def read_sim_GLORYS12V1F(bdys='north', s_year=None, e_year=None):

        ###########################################################################################################################
        ###########################################################################################################################
        ####################################        GLORYS12V1 FREE       ######################################################### 
        ###########################################################################################################################
        ###########################################################################################################################
        LOCBDY='BERING'   
        if bdys == 'south': 
           LOCBDY='RAPID' 

        MYDIR='/data0/project/drakkar/CONFIGS/ORCA12.L50/GLORYS12-V1/CREG12-BDYS/'
        
        print('			READ INPUT DATA FROM  GLORYS12V1 FREE')
        print()

        # Horizontal scale factor 
        file=MYDIR+'GRID/'+'CT_'+bdys+'_mesh_hgr.nc'
        field = Dataset(file)
        cmp_ze1v = npy.squeeze(field.variables['e1v'])
        cmp_lon = npy.squeeze(field.variables['glamt'])
        
        inDIR=MYDIR+'GLORYS12V1-FREE/'
        getsizes_ID=Dataset(inDIR+LOCBDY+'/CT_'+bdys+'_GLORYS12V1-FREE_1m_gridT_201512.nc')
        sizes_ID=npy.array(getsizes_ID['votemper'])

	# A better way and right way to proceed 
        file=MYDIR+'GRID/'+'CT_'+bdys+'_3D_mesh_zgr.nc'
        print(file)
        grd_field=Dataset(file)
        cmp_data_read_dz = npy.squeeze(grd_field.variables['e3v_0'])
        cmp_data_read_depth = npy.squeeze(grd_field.variables['gdept_1d'])
        
        GVcmp_data_read= []  ;  GTcmp_data_read= []  ;   GScmp_data_read= []
        
        Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
        c_year=s_year
        while c_year <= e_year :
                print("                         Read year:", c_year)
                cmp_DIR=MYDIR+'GLORYS12V1-FREE/'+LOCBDY+'/'
                mm=1
                while mm <= 12 :
                        strmm=str(mm) 
                        if mm <= 9 : strmm='0'+str(mm)
                        print("                                 month :", strmm)
                        fileV='CT_'+bdys+'_GLORYS12V1-FREE_1m_gridV_'+str(c_year)+strmm+'.nc'
                        fileT='CT_'+bdys+'_GLORYS12V1-FREE_1m_gridT_'+str(c_year)+strmm+'.nc'
                        fileS='CT_'+bdys+'_GLORYS12V1-FREE_1m_gridS_'+str(c_year)+strmm+'.nc'
                        if c_year == s_year and mm == 1 :
                                field = Dataset(cmp_DIR+fileV)
                                GVcmp_data_read = field.variables['vomecrty']
                                field = Dataset(cmp_DIR+fileT)
                                GTcmp_data_read = field.variables['votemper']
                                field = Dataset(cmp_DIR+fileS)
                                GScmp_data_read = field.variables['vosaline']
                        else:
                                field = Dataset(cmp_DIR+fileV)
                                GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty'],axis=0)
                                field = Dataset(cmp_DIR+fileT)
                                GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper'],axis=0)
                                field = Dataset(cmp_DIR+fileS)
                                GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline'],axis=0)
                        mm+=1
                
                cury=npy.tile(c_year,12)
                Gyears=npy.append(Gyears,cury+t_months)

                c_year+=1
        
        return GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon



def read_sim_GLORYS12V1A(bdys='north', s_year=None, e_year=None):
        ###########################################################################################################################
        ###########################################################################################################################
        ####################################        GLORYS12V1 ORCA12       #######################################################
        ###########################################################################################################################
        ###########################################################################################################################

        MYDIR='/data0/project/drakkar/CONFIGS/ORCA12.L50/GLORYS12-V1/CREG12-BDYS/'
        
        LOCBDY='BERING'
        if bdys == 'south': 
           LOCBDY='RAPID'

        MYDIR='/data0/project/drakkar/CONFIGS/ORCA12.L50/GLORYS12-V1/CREG12-BDYS/'
        
        print(MYDIR )
        print(LOCBDY)
        print('			READ INPUT DATA FROM  GLORYS12V1 ORCA12')
        print 

        # Horizontal scale factor 
        file=MYDIR+'GRID/'+'CT_'+bdys+'_mesh_hgr.nc'
        field = Dataset(file)
        cmp_ze1v = npy.squeeze(field.variables['e1v'])
        cmp_lon = npy.squeeze(field.variables['glamt'])
        
        inDIR=MYDIR+'GLORYS12V1_ORCA12/'
        print(inDIR)
        getsizes_ID=Dataset(inDIR+LOCBDY+'/CT_'+bdys+'_GLORYS12V1_ORCA12_201505_gridT.nc')
        sizes_ID=npy.array(getsizes_ID['votemper'])

	# A better way and right way to proceed 
        file=MYDIR+'GRID/'+'CT_'+bdys+'_3D_mesh_zgr.nc'
        print(file)
        grd_field=Dataset(file)
        cmp_data_read_dz = npy.squeeze(grd_field.variables['e3v_0'])
        cmp_data_read_depth = npy.squeeze(grd_field.variables['gdept_1d'])

        
        GVcmp_data_read= []  ;  GTcmp_data_read= []  ;   GScmp_data_read= []
        
        Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
        c_year=s_year
        while c_year <= e_year :
                print("                         Read year:", c_year)
                cmp_DIR=MYDIR+'GLORYS12V1_ORCA12/'+LOCBDY+'/'
                mm=1
                while mm <= 12 :
                        strmm=str(mm) 
                        if mm <= 9 : strmm='0'+str(mm)
                        fileV='CT_'+bdys+'_GLORYS12V1_ORCA12_'+str(c_year)+strmm+'_gridV.nc'
                        fileT='CT_'+bdys+'_GLORYS12V1_ORCA12_'+str(c_year)+strmm+'_gridT.nc'
                        fileS='CT_'+bdys+'_GLORYS12V1_ORCA12_'+str(c_year)+strmm+'_gridS.nc'
                        if c_year == s_year and mm == 1 :
                                field = Dataset(cmp_DIR+fileV)
                                GVcmp_data_read = field.variables['vomecrty']
                                field = Dataset(cmp_DIR+fileT)
                                GTcmp_data_read = field.variables['votemper']
                                field = Dataset(cmp_DIR+fileS)
                                GScmp_data_read = field.variables['vosaline']
                        else:
                                field = Dataset(cmp_DIR+fileV)
                                GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty'],axis=0)
                                field = Dataset(cmp_DIR+fileT)
                                GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper'],axis=0)
                                field = Dataset(cmp_DIR+fileS)
                                GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline'],axis=0)
                        mm+=1
                
                cury=npy.tile(c_year,12)
                Gyears=npy.append(Gyears,cury+t_months)

                c_year+=1
                
        return GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon


def read_sim_GLORYS12V1AEx(bdys='north', s_year=None, e_year=None):
        ###########################################################################################################################
        ###########################################################################################################################
        ####################################        GLORYS12V1AEx ORCA12    #######################################################
        ###########################################################################################################################
        ###########################################################################################################################

        
        LOCBDY='BERING'
        MYDIR='/data0/project/drakkar/CONFIGS/ORCA12.L50/GLORYS12-V1/CREG12-BDYS/GLORYS12V1_ORCA12/'+LOCBDY+'/'
        ### TEMPO MYDIR='../BERING_20191023_LARGER/'

        if bdys == 'south': 
           LOCBDY='RAPID'
           MYDIR='/data0/project/drakkar/CONFIGS/ORCA12.L50/GLORYS12-V1/CREG12-BDYS/GLORYS12V1_ORCA12/'+LOCBDY+'/'

        
        print(MYDIR )
        print(LOCBDY)
        print('			READ INPUT DATA FROM  GLORYS12V1AEx ORCA12')
        print 
        MYDIRGRD='/data0/project/drakkar/CONFIGS/ORCA12.L50/GLORYS12-V1/CREG12-BDYS/'

        # Horizontal scale factor 
        file=MYDIRGRD+'GRID/'+'CT_'+bdys+'_mesh_hgr.nc'
        field = Dataset(file)
        cmp_ze1v = npy.squeeze(field.variables['e1v'])
        cmp_lon = npy.squeeze(field.variables['glamt'])
        
        # Horizontal scale factor 
        file=MYDIRGRD+'GRID/'+'CT_'+bdys+'_mask.nc'
        field = Dataset(file)
        cmp_tmsk = npy.squeeze(field.variables['tmask'])
        cmp_vmsk = npy.squeeze(field.variables['vmask'])
        
        if bdys == 'north': 
        	inDIR=MYDIR
        	getsizes_ID=Dataset(inDIR+'CT_north_GLORYS12V1_ORCA12_201501_gridT.nc')
        	### TEMPO inDIR=MYDIR+'2010/'
        	### TEMPO getsizes_ID=Dataset(inDIR+'eCREG12-GLYS12-v1-CREG12.L75-BDY_northLarger_T_y2010_noflip.nc')
        else:
        	inDIR=MYDIR
        	getsizes_ID=Dataset(inDIR+'CT_south_GLORYS12V1_ORCA12_201501_gridT.nc')
        print(inDIR)
        sizes_ID=npy.array(getsizes_ID['votemper'])

	# A better way and right way to proceed 
        file=MYDIRGRD+'GRID/'+'CT_'+bdys+'_3D_mesh_zgr.nc'
        print(file)
        grd_field=Dataset(file)
        cmp_data_read_dz = npy.squeeze(grd_field.variables['e3v_0'])
        cmp_data_read_depth = npy.squeeze(grd_field.variables['gdept_1d'])

        
        GVcmp_data_read= []  ;  GTcmp_data_read= []  ;   GScmp_data_read= []
        
        Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
        c_year=s_year
        while c_year <= e_year :
                print("                         Read year:", c_year)
                if bdys == 'north': 
                	### TEMPO   cmp_DIR=MYDIR+str(c_year)+'/'
                	### TEMPO   fileV='eCREG12-GLYS12-v1-CREG12.L75-BDY_northLarger_V_y'+str(c_year)+'_noflip.nc'
                	### TEMPO   fileT='eCREG12-GLYS12-v1-CREG12.L75-BDY_northLarger_T_y'+str(c_year)+'_noflip.nc'
                	### TEMPO   fileS='eCREG12-GLYS12-v1-CREG12.L75-BDY_northLarger_S_y'+str(c_year)+'_noflip.nc'
                	cmp_DIR=MYDIR+'/CONCAT/'
                	fileV='CT_north_GLORYS12V1_ORCA12_'+str(c_year)+'_gridV.nc'
                	fileT='CT_north_GLORYS12V1_ORCA12_'+str(c_year)+'_gridT.nc'
                	fileS='CT_north_GLORYS12V1_ORCA12_'+str(c_year)+'_gridS.nc'
                else:
                	cmp_DIR=MYDIR+'/CONCAT/'
                	fileV='CT_south_GLORYS12V1_ORCA12_'+str(c_year)+'_gridV.nc'
                	fileT='CT_south_GLORYS12V1_ORCA12_'+str(c_year)+'_gridT.nc'
                	fileS='CT_south_GLORYS12V1_ORCA12_'+str(c_year)+'_gridS.nc'
                if c_year == s_year :
                        field = Dataset(cmp_DIR+fileV)
                        GVcmp_data_read = field.variables['vomecrty']*cmp_vmsk
                        field = Dataset(cmp_DIR+fileT)
                        GTcmp_data_read = field.variables['votemper']*cmp_tmsk
                        field = Dataset(cmp_DIR+fileS)
                        GScmp_data_read = field.variables['vosaline']*cmp_tmsk
                else:
                	field = Dataset(cmp_DIR+fileV)
                	GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty']*cmp_vmsk,axis=0)
                	field = Dataset(cmp_DIR+fileT)
                	GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper']*cmp_tmsk,axis=0)
                	field = Dataset(cmp_DIR+fileS)
                	GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline']*cmp_tmsk,axis=0)
                
                cury=npy.tile(c_year,12)
                Gyears=npy.append(Gyears,cury+t_months)
                
                c_year+=1
                
        return GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon


def read_sim_GLORYS12V1AExMerc(bdys='north', s_year=None, e_year=None):
        ###########################################################################################################################
        ###########################################################################################################################
        ####################################        GLORYS12V1ExMerc ORCA12       #################################################
        ###########################################################################################################################
        ###########################################################################################################################

        LOCBDY='BERING'
        if bdys == 'south': 
           LOCBDY='RAPID'

        MYDIR='../DATA-FROM-CMEMS-MERC/'+LOCBDY+'/'
        
        
        print(MYDIR )
        print(LOCBDY)
        print()
        print('			READ INPUT DATA FROM  GLORYS12V1ExMerc ORCA12')
        print 
        MYDIRGRD=MYDIR
        # Vertical scale factor 
        file=MYDIRGRD+LOCBDY+'_ext-PSY4V3R1_3D_mesh_zgr.nc'
        print(file)
        grd_field=Dataset(file)
        cmp_data_read_dz = npy.squeeze(grd_field.variables['e3v_0'])
        cmp_data_read_depth = npy.squeeze(grd_field.variables['gdept_1d'])

        # Horizontal scale factor 
        file=MYDIRGRD+'/'+LOCBDY+'_ext-PSY4V3R1_mesh_hgr.nc'
        field = Dataset(file)
        cmp_ze1v = npy.squeeze(field.variables['e1v'])
        cmp_lon = npy.squeeze(field.variables['glamt'])

	# Velocities Mask 
        file=MYDIRGRD+'/'+LOCBDY+'_ext-PSY4V3R1_mask.nc'
        field = Dataset(file)
        cmp_vmsk = npy.squeeze(field.variables['vmask'])
        cmp_tmsk = npy.squeeze(field.variables['tmask'])
        
        inDIR=MYDIR
        print(inDIR)
        getsizes_ID=Dataset(inDIR+'ext-GLORYS12V1_1mAV_y2016.1m_gridT_4INTERP.nc')
        sizes_ID=npy.array(getsizes_ID['votemper'])

        GVcmp_data_read= []  ;  GTcmp_data_read= []  ;   GScmp_data_read= []
        
        Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
        c_year=s_year
        while c_year <= e_year :
                print("                         Read year:", c_year)
                cmp_DIR=MYDIR+'/'
                fileV='ext-GLORYS12V1_1mAV_y'+str(c_year)+'.1m_gridV_4INTERP.nc'
                fileT='ext-GLORYS12V1_1mAV_y'+str(c_year)+'.1m_gridT_4INTERP.nc'
                fileS='ext-GLORYS12V1_1mAV_y'+str(c_year)+'.1m_gridS_4INTERP.nc'
                if c_year == s_year :
                        field = Dataset(cmp_DIR+fileV)
                        GVcmp_data_read = field.variables['vomecrty']*cmp_vmsk
                        field = Dataset(cmp_DIR+fileT)
                        GTcmp_data_read = field.variables['votemper']*cmp_tmsk
                        field = Dataset(cmp_DIR+fileS)
                        GScmp_data_read = field.variables['vosaline']*cmp_tmsk
                else:
                	field = Dataset(cmp_DIR+fileV)
                	GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty']*cmp_vmsk,axis=0)
                	field = Dataset(cmp_DIR+fileT)
                	GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper']*cmp_tmsk,axis=0)
                	field = Dataset(cmp_DIR+fileS)
                	GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline']*cmp_tmsk,axis=0)
                
                cury=npy.tile(c_year,12)
                Gyears=npy.append(Gyears,cury+t_months)

                c_year+=1
                
        return GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon


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
        print('			READ INPUT DATA FROM  GLORYS12V1 interpolated on the CREG12.L75-REF09 grid')
        print 
        MYDIRGRD='./'
        # Vertical scale factor 
        file=MYDIRGRD+'CREG12.L75-REF09_mesh_mask_Bering_Glorys12v1_Tgt.nc'
        field = Dataset(file)
        cmp_data_read_dz = npy.squeeze(field.variables['e3v_0'])
        cmp_data_read_depth = npy.squeeze(field.variables['gdept_1d'])
        # Horizontal scale factor 
        file=MYDIRGRD+'CREG12.L75-REF09_mesh_mask_Bering_Glorys12v1_Tgt.nc'
        field = Dataset(file)
        cmp_ze1v = npy.squeeze(field.variables['e1v'])
        cmp_lon = npy.squeeze(field.variables['glamt'])

	# Velocities Mask 
        file=MYDIRGRD+'CREG12.L75-REF09_mesh_mask_Bering_Glorys12v1_Tgt.nc'
        field = Dataset(file)
        cmp_vmsk = npy.squeeze(field.variables['vmask'])
        cmp_tmsk = npy.squeeze(field.variables['tmask'])

        inDIR='/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/BDYS/BERING/'
        print(inDIR)
	# Read 1 file just to get dim. size
        getsizes_ID=Dataset(inDIR+'ALL/GLORYS12V1-CREG12.L75_BERING_y1999.1d_gridT.nc')
        sizes_ID=npy.array(getsizes_ID['votemper'])
        
        GVcmp_data_read= []  ;  GTcmp_data_read= []  ;   GScmp_data_read= []
        
        Gyears=[]     ;      t_months=(npy.arange(365)+0.5)/365.
        c_year=s_year
        while c_year <= e_year :
                print("                         Read year:", c_year)
                cmpT_DIR=inDIR+'/ALL/'
                cmpV_DIR=inDIR+str(c_year)+'/NO-COR/'
                fileV='GLORYS12V1-CREG12.L75_BERING_y'+str(c_year)+'.1d_gridV.nc'
                fileT='GLORYS12V1-CREG12.L75_BERING_y'+str(c_year)+'.1d_gridT.nc'
                fileS='GLORYS12V1-CREG12.L75_BERING_y'+str(c_year)+'.1d_gridS.nc'
                if c_year == s_year :
                        field = Dataset(cmpV_DIR+fileV)
                        GVcmp_data_read = field.variables['vomecrty']
                        #GVcmp_data_read = field.variables['vomecrty']*cmp_vmsk
                        field = Dataset(cmpT_DIR+fileT)
                        GTcmp_data_read = field.variables['votemper']
                        #GTcmp_data_read = field.variables['votemper']*cmp_tmsk
                        field = Dataset(cmpT_DIR+fileS)
                        GScmp_data_read = field.variables['vosaline']
                        #GScmp_data_read = field.variables['vosaline']*cmp_tmsk
                else:
                	field = Dataset(cmpV_DIR+fileV)
                	GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty'],axis=0)
                	#GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty']*cmp_vmsk,axis=0)
                	field = Dataset(cmpT_DIR+fileT)
                	GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper'],axis=0)
                	#GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper']*cmp_tmsk,axis=0)
                	field = Dataset(cmpT_DIR+fileS)
                	GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline'],axis=0)
                	#GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline']*cmp_tmsk,axis=0)
                
                cury=npy.tile(c_year,365)
                Gyears=npy.append(Gyears,cury+t_months)

                c_year+=1
                
        return GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon


def read_sim_MJMgd16(bdys='north', s_year=None, e_year=None):
                ###########################################################################################################################
                ###########################################################################################################################
                ###########################          EORCA12.L75-MJMgd16             ######################################################
                ###########################################################################################################################
                ###########################################################################################################################
                LOCBDY='BERING'   
                if bdys == 'south': 
                   LOCBDY='RAPID' 

                MYDIR='/data0/project/drakkar/CONFIGS/ORCA12.L75/EORCA12.L75-MJMgd16-MEAN/BDYS-FOR-CREG/'
                
                print('			READ INPUT DATA FROM EORCA12.L75-MJMgd16 ')
                print()
		# Velocities Mask 
                file=MYDIR+'GRID/'+LOCBDY+'12.L75-MJMgd16_mask.nc'
                field = Dataset(file)
                cmp_vmsk = npy.squeeze(field.variables['vmask'])
                cmp_tmsk = npy.squeeze(field.variables['tmask'])
                
                # Vertical scale factor 
                file=MYDIR+'GRID/'+LOCBDY+'12.L75-MJMgd16_mesh_zgr.nc'
                field = Dataset(file)
                cmp_data_read_dz = npy.squeeze(field.variables['e3v_0'])*cmp_vmsk[:,:,:]
                cmp_data_read_depth = npy.squeeze(field.variables['gdept_1d'])
                # Horizontal scale factor 
                file=MYDIR+'GRID/'+LOCBDY+'12.L75-MJMgd16_mesh_hgr.nc'
                field = Dataset(file)
                cmp_ze1v = npy.squeeze(field.variables['e1v'])*cmp_vmsk[0,:,:]
                cmp_lon = npy.squeeze(field.variables['glamt'])

                inDIR=MYDIR+LOCBDY+'12.L75-MJMgd16-MEAN/'
                getsizes_ID=Dataset(inDIR+LOCBDY+'12.L75-MJMgd16_y2015m12.5d_gridT.nc')
                sizes_ID=npy.array(getsizes_ID['votemper'])
                
                GVcmp_data_read= []  ;  GTcmp_data_read= []  ;   GScmp_data_read= []
                
                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        print("                         Read MJMgd16 year:", c_year)
                        cmp_DIR=MYDIR+LOCBDY+'12.L75-MJMgd16-MEAN/'
                        mm=1
                        while mm <= 12 :
                                strmm=str(mm) 
                                if mm <= 9 : strmm='0'+str(mm)
                                fileV=LOCBDY+'12.L75-MJMgd16_y'+str(c_year)+'m'+strmm+'.5d_gridV.nc'
                                fileT=LOCBDY+'12.L75-MJMgd16_y'+str(c_year)+'m'+strmm+'.5d_gridT.nc'
                                fileS=LOCBDY+'12.L75-MJMgd16_y'+str(c_year)+'m'+strmm+'.5d_gridT.nc'
                                if c_year == s_year and mm == 1 :
                                        field = Dataset(cmp_DIR+fileV)
                                        GVcmp_data_read = field.variables['vomecrty']*cmp_vmsk
                                        field = Dataset(cmp_DIR+fileT)
                                        GTcmp_data_read = field.variables['votemper']*cmp_tmsk
                                        field = Dataset(cmp_DIR+fileS)
                                        GScmp_data_read = field.variables['vosaline']*cmp_tmsk
                                else:
                                        field = Dataset(cmp_DIR+fileV)
                                        GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty']*cmp_vmsk,axis=0)
                                        field = Dataset(cmp_DIR+fileT)
                                        GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper']*cmp_tmsk,axis=0)
                                        field = Dataset(cmp_DIR+fileS)
                                        GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline']*cmp_tmsk,axis=0)
                                mm+=1
                        
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)

                        c_year+=1


                return GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon


def read_sim_GJM2020(bdys='north', s_year=None, e_year=None):
                ###########################################################################################################################
                ###########################################################################################################################
                ###########################          eORCA12.L75-GJM2020             ######################################################
                ###########################################################################################################################
                ###########################################################################################################################
                LOCBDY='BERING'   
                if bdys == 'south': 
                   LOCBDY='RAPID' 

                MYDIR='/data0/project/drakkar/CONFIGS/ORCA12.L75/eORCA12.L75-GJM2020-MEAN/BERING/'
                
                print('			READ INPUT DATA FROM eORCA12.L75-GJM2020 ')
                print 
		# Velocities Mask 
                file=MYDIR+'GRID/eORCA12.L75_'+LOCBDY+'_byte_mask.nc'
                field = Dataset(file)
                cmp_vmsk = npy.squeeze(field.variables['vmask'])
                cmp_tmsk = npy.squeeze(field.variables['tmask'])
                
                cmp_vmsk3D = npy.tile(cmp_vmsk,(12,1,1,1))
                cmp_tmsk3D = npy.tile(cmp_tmsk,(12,1,1,1))

                # Vertical scale factor 
                file=MYDIR+'GRID/eORCA12.L75_'+LOCBDY+'_mesh_zgr.nc'
                field = Dataset(file)
                cmp_data_read_dz = npy.squeeze(field.variables['e3v_0'])*cmp_vmsk[:,:,:]
                cmp_data_read_depth = npy.squeeze(field.variables['gdept_1d'])
                # Horizontal scale factor 
                file=MYDIR+'GRID/eORCA12.L75_'+LOCBDY+'_mesh_hgr.nc'
                field = Dataset(file)
                cmp_ze1v = npy.squeeze(field.variables['e1v'])*cmp_vmsk[0,:,:]
                cmp_lon = npy.squeeze(field.variables['glamt'])

                inDIR=MYDIR+'/ALL/'
                getsizes_ID=Dataset(inDIR+'eORCA12.L75-GJM2020_BERING_y2010.1m_gridT.nc')
                sizes_ID=npy.array(getsizes_ID['votemper'])
                #print(sizes_ID)
                #print(getsizes_ID['votemper'].shape)
                #print(cmp_vmsk3D.shape)
                
                GVcmp_data_read= npy.empty(cmp_vmsk3D.shape)  ;  GTcmp_data_read= npy.empty(cmp_tmsk3D.shape)   ;   GScmp_data_read= npy.empty(cmp_tmsk3D.shape)
                #GVcmp_data_read= []  ;  GTcmp_data_read= []  ;   GScmp_data_read= []
                
                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        print("                         Read GJM2020 year:", c_year)
                        cmp_DIR=MYDIR+'/ALL/'
                        fileV='eORCA12.L75-GJM2020_'+LOCBDY+'_y'+str(c_year)+'.1m_gridV.nc'
                        fileT='eORCA12.L75-GJM2020_'+LOCBDY+'_y'+str(c_year)+'.1m_gridT.nc'
                        fileS='eORCA12.L75-GJM2020_'+LOCBDY+'_y'+str(c_year)+'.1m_gridT.nc'
                        field = Dataset(cmp_DIR+fileV)
                        #print('votemper.shape',field.variables['vomecrty'].shape)
                        #GVcmp_data_read = field.variables['vomecrty']*cmp_vmsk3D
                        #GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty']*cmp_vmsk3D)
                        GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty']*cmp_vmsk3D,axis=0)
                        field = Dataset(cmp_DIR+fileT)
                        #GTcmp_data_read = field.variables['votemper']*cmp_tmsk3D
                        #GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper']*cmp_tmsk3D)
                        GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper']*cmp_tmsk3D,axis=0)
                        field = Dataset(cmp_DIR+fileT)
                        #GScmp_data_read = field.variables['vosaline']*cmp_tmsk3D
                        #GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline']*cmp_tmsk3D)
                        GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline']*cmp_tmsk3D,axis=0)
                        
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)

                        c_year+=1

                return GVcmp_data_read[12::,:,:,:], GTcmp_data_read[12::,:,:,:], GScmp_data_read[12::,:,:,:], cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon



def read_sim_GLORYS2V4(bdys='north', s_year=None, e_year=None):
                ###########################################################################################################################
                ###########################################################################################################################
                ###########################                 GLORYS2V4                ######################################################
                ###########################################################################################################################
                ###########################################################################################################################
                
                
                print("			READ INPUT DATA FROM GLORYS2V4 ")
                print 
                # Vertical scale factor 
                file='/data0/project/drakkar/CONFIGS/ORCA025.L75/GLORYS2V4/CREG025-BDYS/GRID/obc_'+bdys+'_e3t.nc'
                field = Dataset(file)
                cmp_data_read_dz = npy.squeeze(field.variables['e3t'])
                # Horizontal scale factor 
                file='/data0/project/drakkar/CONFIGS/ORCA025.L75/GLORYS2V4/CREG025-BDYS/GRID/obc_'+bdys+'_e1v.nc'
                field = Dataset(file)
                cmp_ze1v = npy.squeeze(field.variables['e1v'])
                cmp_lon = npy.squeeze(field.variables['glamt'])
                # Depth of T-Point
                file='/data0/project/drakkar/CONFIGS/ORCA025.L75/GLORYS2V4/CREG025-BDYS/GRID/obc_'+bdys+'_gdept.nc'
                field = Dataset(file)
                cmp_data_read_depth = npy.squeeze(field.variables['gdept_0'])

                LOCBDY='BERING'   
                if bdys == 'south': LOCBDY='RAPID' 
                GloinDIR='/data0/project/drakkar/CONFIGS/ORCA025.L75/GLORYS2V4/CREG025-BDYS/'+LOCBDY+'/'
                getsizes_ID=Dataset(GloinDIR+'obc_'+bdys+'_y2016_T.nc')
                sizes_ID=npy.array(getsizes_ID['votemper'])
                
                GVcmp_data_read= []  ;  GTcmp_data_read= []  ;   GScmp_data_read= []
                
                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        print("                         Read GLORYS2V4 year:", c_year)
                        cmp_DIR='/data0/project/drakkar/CONFIGS/ORCA025.L75/GLORYS2V4/CREG025-BDYS/'+LOCBDY+'/'
                        fileV='obc_'+bdys+'_y'+str(c_year)+'_V.nc'
                        fileT='obc_'+bdys+'_y'+str(c_year)+'_T.nc'
                        fileS='obc_'+bdys+'_y'+str(c_year)+'_S.nc'
                        if c_year == s_year:
                                field = Dataset(cmp_DIR+fileV)
                                GVcmp_data_read = npy.squeeze(field.variables['vomecrty'])
                                field = Dataset(cmp_DIR+fileT)
                                GTcmp_data_read = npy.squeeze(field.variables['votemper'])
                                field = Dataset(cmp_DIR+fileS)
                                GScmp_data_read = npy.squeeze(field.variables['vosaline'])
                        else:
                                field = Dataset(cmp_DIR+fileV)
                                GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty'],axis=0)
                                field = Dataset(cmp_DIR+fileT)
                                GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper'],axis=0)
                                field = Dataset(cmp_DIR+fileS)
                                GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline'],axis=0)
                
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)

                        c_year+=1


                return GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon



def read_sim_GJM189(bdys='north', s_year=None, e_year=None):
                ###########################################################################################################################
                ###########################################################################################################################
                ###########################           ORCA025.L75-GJM189             ######################################################
                ###########################################################################################################################
                ###########################################################################################################################
                
                
                print("			READ INPUT DATA FROM ORCA025.L75-GJM189 ")
                print 
                # Vertical scale factor 
                file='/data0/project/drakkar/CONFIGS/CREG025.L75/DATA_FORCING/BDYS/IA-GJM189/ALL/ORCA025.L75-GJM189-CREG025.L75-BDY_'+bdys+'_V_y2010.nc'
                field = Dataset(file)
                cmp_data_read_dz = npy.squeeze(field.variables['e3v'])
                # Horizontal scale factor 
                file='/data0/project/drakkar/CONFIGS/CREG025.L75/DATA_FORCING/BDYS/IA-GJM189/ALL/ORCA025.L75-GJM189-CREG025.L75-BDY_'+bdys+'_V_y2010.nc'
                field = Dataset(file)
                cmp_ze1v = npy.squeeze(field.variables['e1v'])
                cmp_lon = npy.squeeze(field.variables['nav_lon'])
                # Depth of T-Point
                file='/data0/project/drakkar/CONFIGS/CREG025.L75/DATA_FORCING/BDYS/IA-GJM189/ALL/ORCA025.L75-GJM189-CREG025.L75-BDY_'+bdys+'_T_y2010.nc'
                field = Dataset(file)
                cmp_data_read_depth = npy.squeeze(field.variables['deptht'])

                LOCBDY='BERING'   
                if bdys == 'south': LOCBDY='RAPID' 
                GloinDIR='/data0/project/drakkar/CONFIGS/CREG025.L75/DATA_FORCING/BDYS/IA-GJM189/ALL/'
                getsizes_ID=Dataset(GloinDIR+'ORCA025.L75-GJM189-CREG025.L75-BDY_'+bdys+'_T_y2010.nc')
                sizes_ID=npy.array(getsizes_ID['votemper'])
                
                GVcmp_data_read= []  ;  GTcmp_data_read= []  ;   GScmp_data_read= []
                
                Gyears=[]     ;      t_months=(npy.arange(12)+0.5)/12.
                c_year=s_year
                while c_year <= e_year :
                        print("                         Read ORCA025.L75-GJM189 year:", c_year)
                        cmp_DIR='/data0/project/drakkar/CONFIGS/CREG025.L75/DATA_FORCING/BDYS/IA-GJM189/ALL/'
                        fileV='ORCA025.L75-GJM189-CREG025.L75-BDY_'+bdys+'_V_y'+str(c_year)+'.nc'
                        fileT='ORCA025.L75-GJM189-CREG025.L75-BDY_'+bdys+'_T_y'+str(c_year)+'.nc'
                        fileS='ORCA025.L75-GJM189-CREG025.L75-BDY_'+bdys+'_S_y'+str(c_year)+'.nc'
                        if c_year == s_year:
                                field = Dataset(cmp_DIR+fileV)
                                GVcmp_data_read = npy.squeeze(field.variables['vomecrty'])
                                field = Dataset(cmp_DIR+fileT)
                                GTcmp_data_read = npy.squeeze(field.variables['votemper'])
                                field = Dataset(cmp_DIR+fileS)
                                GScmp_data_read = npy.squeeze(field.variables['vosaline'])
                        else:
                                field = Dataset(cmp_DIR+fileV)
                                GVcmp_data_read = npy.append(GVcmp_data_read,field.variables['vomecrty'],axis=0)
                                field = Dataset(cmp_DIR+fileT)
                                GTcmp_data_read = npy.append(GTcmp_data_read,field.variables['votemper'],axis=0)
                                field = Dataset(cmp_DIR+fileS)
                                GScmp_data_read = npy.append(GScmp_data_read,field.variables['vosaline'],axis=0)
                
                        cury=npy.tile(c_year,12)
                        Gyears=npy.append(Gyears,cury+t_months)

                        c_year+=1


                return GVcmp_data_read, GTcmp_data_read, GScmp_data_read, cmp_data_read_depth, cmp_ze1v, cmp_data_read_dz, sizes_ID, cmp_lon

