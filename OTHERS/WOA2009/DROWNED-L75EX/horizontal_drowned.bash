#!/bin/bash

set -x

# 1- Extract just field temperature or salinity depending the input file 
# 2- add the missing_value attribute. This step is required to drown fields 
#    over land areas using sosie package

res=1 # 1 is the one available resolution

cd OPERATE
ln -sf ../sosie.x .
ln -sf ../mask_field.nc .
ln -sf ../deptht_L75.nc .

for var in `echo salinity temperature ` ; do
        if [ $var = 'temperature' ] ; then
           svar='temperature'
           namv='t_an'
        else
           svar='salinity'
           namv='s_an'
        fi
	ln -sf ../namelist_woa09_${namv}_drownfields .
        ln -sf ../COMBINED/woa09_${svar}_monthly_${res}deg_${namv}_CMA.nc input_field.nc

	./sosie.x -f namelist_woa09_${namv}_drownfields
	mv ${namv}_WOA09-360x180_drowned.nc ../CMA_DROWNED/woa09_${svar}_monthly_${res}deg_${namv}_CMA_drowned.nc 

done

cd ../
