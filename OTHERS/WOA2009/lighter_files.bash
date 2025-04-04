#!/bin/bash

set -x

# 1- Extract just field temperature or salinity depending the input file 
# 2- add the missing_value attribute. This step is required to drown fields 
#    over land areas using sosie package

res=1 # either 1 or 4 for the 1deg or 0.25deg resolution

for var in `echo temperature salinity` ; do
        if [ $var = 'temperature' ] ; then
	   svar='temperature'
	   namv='t_an'
	else 
	   svar='salinity'
	   namv='s_an'
	fi
	for freq in `echo annual seasonal monthly`  ; do
	     ncks -v ${namv},depth,lat,lon  woa09_${svar}_${freq}_${res}deg.nc woa09_${svar}_${freq}_${res}deg_${namv}_tmp.nc   
	     ncatted -a missing_value,${namv},c,f,9.96921e+36 woa09_${svar}_${freq}_${res}deg_${namv}_tmp.nc
	     ncks --mk_rec_dmn time woa09_${svar}_${freq}_${res}deg_${namv}_tmp.nc woa09_${svar}_${freq}_${res}deg_${namv}.nc
	     mv woa09_${svar}_${freq}_${res}deg_${namv}.nc ./MODIFIED/.
	     rm -f woa09_${svar}_${freq}_${res}deg_${namv}_tmp.nc
	done 

done

