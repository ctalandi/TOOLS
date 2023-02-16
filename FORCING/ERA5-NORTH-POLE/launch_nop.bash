#!/bin/bash

set -xv 

SY=1986
EY=1995

for cyear in `seq $SY $EY ` ; do 

	#for gtype in `echo t2m `; do 
	for gtype in `echo u10 v10 d2m t2m msr mtpr msl msdwswrf msdwlwrf` ; do 

		sed -e "s/<XXYEARXX>/${cyear}/"  -e "s/<XXVARGRDXX>/${gtype}/" \
                    Job_ERA5_NOP.slurm.tmp> ./JOBS/Job_ERA5_NOP_y${cyear}_${gtype}.slurm
		
		qsub ./JOBS/Job_ERA5_NOP_y${cyear}_${gtype}.slurm

	done
done 
