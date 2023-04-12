#!/bin/python

import numpy as npy
import matplotlib.pylab as plt 

def read_obsBERING(ef_year=2017, make_plot=False):
        #----------------------------------------------------------------------------------------
        # Structure of the ASCII file BeringStrait_Monthlymeans_TRANSPORT_Jun2017.txt or 2021 one
        #% Mooring  Year    Month   Mean  Error        MeanCorr  Error
        
        extnam='Jun2017' 
        if ef_year == 2021 : extnam='Jan2021'
        dir='./OBS-BERING/'   ; file='BeringStrait_Monthlymeans_TRANSPORT_'+extnam+'.txt'
        
        # Open file
        f = open(dir+file,'r')
        
        # Read and ignore header lines
        skip=0  ; ltoskip=40
        if ef_year == 2021 :  ltoskip=48
        while skip <= ltoskip-1 : 
                header1 = f.readline()
                skip+=1
        
        
        # Loop over lines and extract variables of interest
        transp_A3MeanCorr=[]
        for line in f:
               line = line.strip()
               columns = line.split()
               transp_A3MeanCorr = npy.append(transp_A3MeanCorr,float(columns[5]))
        f.close()
        
        # UNITS: Sv
        
        #----------------------------------------------------------------------------------------
        # Structure of the ASCII file BeringStrait_Monthlymeans_FW_Jun2017.txt or 2021 one
        #% Mooring  Year    Month   Mean  Error        Mean  Error
        
        dir='./OBS-BERING/'   ; file='BeringStrait_Monthlymeans_FW_'+extnam+'.txt'
        
        # Open file
        f = open(dir+file,'r')
        
        # Read and ignore header lines
        skip=0  ; ltoskip=41
        if ef_year == 2021 :  ltoskip=49
        while skip <= ltoskip-1 : 
                header1 = f.readline()
                skip+=1
        
        # Loop over lines and extract variables of interest
        FW_A3FWcorr=[] 
        for line in f:
               line = line.strip()
               columns = line.split()
               FW_A3FWcorr = npy.append(FW_A3FWcorr,float(columns[5]))
        f.close()
        
        # UNITS: km3
        
        #----------------------------------------------------------------------------------------
        # Structure of the ASCII file BeringStrait_Monthlymeans_HEAT_Jun2017.txt or 2021 one
        #
        
        dir='./OBS-BERING/'   ; file='BeringStrait_Monthlymeans_HEAT_'+extnam+'.txt'
        
        # Open file
        f = open(dir+file,'r')
        
        # Read and ignore header lines
        skip=0  ; ltoskip=41
        if ef_year == 2021 :  ltoskip=49
        while skip <= ltoskip-1 : 
                header1 = f.readline()
                skip+=1
        
        # Loop over lines and extract variables of interest
        HT_A3heatCorr=[] 
        for line in f:
               line = line.strip()
               columns = line.split()
               HT_A3heatCorr = npy.append(HT_A3heatCorr,float(columns[5]))
        f.close()
        
        # UNITS: 10^20 J
        
        years=[]
        t_months=(npy.arange(12)+0.5)/12.
        c_year=1990.
        while c_year <= 2016:
           cury=npy.tile(c_year,12)
           years=npy.append(years,cury+t_months)
           c_year+=1
        
        
        npy.savez('./OBS-BERING/WOODGATE-Obs_BeringStrait_Monthlymeans_FWHeatTrans_'+extnam+'.npz', transp_A3MeanCorr=transp_A3MeanCorr, FW_A3FWcorr=FW_A3FWcorr, HT_A3heatCorr=HT_A3heatCorr, YearsObs=years)
        
        
        if make_plot:
        
                 #-------------------------------------------------------------------------------------------------
                 plt.figure()
                 
                 plt.subplot(311)
                 plt.title('Bering Strait Monthly means \n from Woodgate et al. PO2017', size=8)
                 plt.plot(years,transp_A3MeanCorr,'-o')
                 plt.xlim([1990,2016])
                 plt.ylabel('Estimated transport A3 \n (Sv)',size=7)
                 plt.xticks(size=7)
                 plt.yticks(size=7)
                 plt.grid(True,linestyle='--', color='grey',alpha=0.7)
                 
                 plt.subplot(312)
                 plt.plot(years,FW_A3FWcorr,'-o')
                 plt.xlim([1990,2016])
                 plt.ylabel('Estimated FW transport A3FWcorr \n'+r'(km$^3$)',size=7)
                 plt.xticks(size=7)
                 plt.yticks(size=7)
                 plt.grid(True,linestyle='--', color='grey',alpha=0.7)
                 
                 plt.subplot(313)
                 plt.plot(years,HT_A3heatCorr,'-o')
                 plt.xlim([1990,2016])
                 plt.ylabel('Estimated Heat transport A3heatCorr \n'+r'(10$^{20}$ J)',size=7)
                 plt.xticks(size=7)
                 plt.yticks(size=7)
                 plt.grid(True,linestyle='--', color='grey',alpha=0.7)
                 
                 plt.tight_layout()
                 plt.savefig('BeringStrait_monthlymeans_'+extnam+'.pdf')
        

        return transp_A3MeanCorr, FW_A3FWcorr, HT_A3heatCorr, years
        
