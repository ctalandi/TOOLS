#!/bin/bash

set -xv 

SY=2007
EY=2021

#for gtype in `echo  t2m d2m msr mtpr msl msdwswrf msdwlwrf`; do 
for gtype in `echo  w10 wu10 wv10 ` ; do 

	sed -e "s/<XXYEARXX>/${cyear}/"  -e "s/<XXVARGRDXX>/${gtype}/" \
	    -e "s/<XXYEAR1XX>/${SY}/"  -e "s/<XXYEAR2XX>/${EY}/" \
	       metamake_climato.sh.tmp > ./JOBS/metamake_climato_y${SY}-${EY}_${gtype}.slurm
	
	qsub ./JOBS/metamake_climato_y${SY}-${EY}_${gtype}.slurm

done 
