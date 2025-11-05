#!/bin/bash

set -xv 

Y_S=1985
Y_E=1985

# For ERA5
for year in `seq ${Y_S} ${Y_E} `; do 

	sed -e "s/<XXYEARXX>/${year}/g" namelist_bilin_era5_skt > ./NAM/namelist_bilin_era5_skt_y${year}
	sed -e "s/<XXYEARXX>/${year}/g" Job_interp_era5_skt.pbs > ./JOBS/Job_interp_era5_skt_y${year}.pbs 
	qsub ./JOBS/Job_interp_era5_skt_y${year}.pbs 

done 


# For The mean seasonal cycle correction relying on differences between ERA5 & JRA55
for mm in `seq -w 02 02 `; do

	sed -e "s/<XXMONTHXX>/${mm}/g"  namelist_bilin_jra5_CREG025.L75 > ./NAM/namelist_bilin_jra5Seas_m${mm}
	sed -e "s/<XXMONTHXX>/${mm}/g"  Job_interp_jra5Seas.pbs > ./JOBS/Job_interp_jra5Seas_m${mm}.pbs
	qsub ./JOBS/Job_interp_jra5Seas_m${mm}.pbs

done

