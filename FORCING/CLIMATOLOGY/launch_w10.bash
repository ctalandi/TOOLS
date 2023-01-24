#!/bin/bash

set -xv 

SY=2007
EY=2021

for var in `echo  w10 `; do 

	for cyear in `seq $SY $EY `; do 

		sed -e "s/<XXYEARXX>/${cyear}/"  -e "s/<XXVARGRDXX>/${var}/" \
		       metamake_w10_w10xu.sh.tmp > ./JOBS/metamake_w10_w10xu_y${cyear}_${var}.slurm
		
		qsub ./JOBS/metamake_w10_w10xu_y${cyear}_${var}.slurm

	done 
done 
