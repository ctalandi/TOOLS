#!/bin/bash

set -x

# 1- Extract just field temperature or salinity depending the input file 
# 2- add the missing_value attribute. This step is required to drown fields 
#    over land areas using sosie package

res=1 # 1 is the one available resolution
smo=1 # Smoothing level 

cd OPERATE
# Rely on the Sosie release 3.0 (Git Master) version (important for the namelist)
ln -sf /home1/datahome/ctalandi/DEV/SOSIE_GIT_MASTER/bin/sosie3.x .
ln -sf ../woa09_3Dmsk_1deg.nc  mask_field.nc 
ln -sf ../deptht_L75.nc .

for var in `echo salinity temperature ` ; do
        if [ $var = 'temperature' ] ; then
           svar='temperature'
           namv='t_an'
        else
           svar='salinity'
           namv='s_an'
        fi
	ln -sf ../namelist_woa09_${namv}_drownfields_soGitMaster .
        ln -sf ../DATA/woa09_${svar}_monthly_${res}deg_${namv}_CMA_SM${smo}_4So.nc input_field.nc

	./sosie3.x -f namelist_woa09_${namv}_drownfields_soGitMaster
	mv ${namv}_WOA09-Z75_WOA09_360x180_drowned.nc ../CMA_DROWNED/woa09_${svar}_monthly_${res}deg_${namv}_CMA_SM${smo}_drowned.nc 

done

cd ../
