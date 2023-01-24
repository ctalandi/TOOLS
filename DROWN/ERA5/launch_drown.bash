#!/bin/bash

set -xv 

SY=2019
EY=2020

for cyear in `seq $SY $EY ` ; do 

	for gtype in `echo u10 v10 d2m t2m msr mtpr msl msdwswrf msdwlwrf` ; do 

		sed -e "s/<XXYEARXX>/${cyear}/"  -e "s/<XXVARGRDXX>/${gtype}/" \
                    Sosie_ERA5_drown.slurm.tmp > ./JOBS/Sosie_ERA5_drown_y${cyear}_${gtype}.slurm
		
		qsub ./JOBS/Sosie_ERA5_drown_y${cyear}_${gtype}.slurm

	done
done 
