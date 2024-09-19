#!/bin/bash

set -xv 

Y_S=1985
Y_E=1985

for year in `seq ${Y_S} ${Y_E} `; do 

	sed -e "s/<XXYEARXX>/${year}/g" namelist_bilin_era5_skt > ./NAM/namelist_bilin_era5_skt_y${year}
	sed -e "s/<XXYEARXX>/${year}/g" Job_interp_era5_skt.pbs > ./JOBS/Job_interp_era5_skt_y${year}.pbs 
	qsub ./JOBS/Job_interp_era5_skt_y${year}.pbs 

done 
