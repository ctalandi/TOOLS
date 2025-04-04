#!/bin/bash

set -x

# 1- Add missing value in file
# 2- Change the record time_counter because SOSIE need it (why ?) not done 
# 3- Add lat lon depth fields that have been removed by hand using the command line: 
#    ncks -v lat,lon,depth woa09_salinity_seasonal_1deg.nc woa09_salinity_seasonal_1deg_genvar.nc
# 4- Add a right axis time (extracted from the woa09_salinity_seasonal_1deg.nc) file using the command line:
#    ncks -v time woa09_salinity_monthly_1deg.nc woa09_monthly_time.nc 
#    rename -v time,time_counter woa09_monthly_time.nc  

pwd

res=1 # 1 is the only resolution available

for var in `echo temperature salinity` ; do
        if [ $var = 'temperature' ] ; then
           svar='temperature'
           namv='t_an'
        else
           svar='salinity'
           namv='s_an'
        fi


        ncatted -a missing_value,${namv},c,f,9.96921e+36 woa09_${svar}_monthly_${res}deg_${namv}_CMA.nc
        #ncks -O --mk_rec_dmn time_counter woa09_${svar}_monthly_${res}deg_${namv}_CMA.nc woa09_${svar}_monthly_${res}deg_${namv}_CMA.nc
	ncks -A woa09_salinity_seasonal_1deg_genvar.nc woa09_${svar}_monthly_${res}deg_${namv}_CMA.nc
        ncks -A woa09_monthly_time.nc woa09_${svar}_monthly_${res}deg_${namv}_CMA.nc 

done

