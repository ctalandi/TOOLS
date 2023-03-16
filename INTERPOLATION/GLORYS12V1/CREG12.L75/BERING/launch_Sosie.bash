#!/bin/bash

set -xv 

SY=2022
EY=2022

for cyear in `seq $SY $EY ` ; do 

	#for gtype in `echo  gridT gridS gridU gridV ` ; do 
	#for gtype in `echo gridT gridS gridU gridV ` ; do 
	for gtype in `echo icemod  ` ; do 
	#for gtype in `echo gridT gridS gridU gridV grid2D icemod ` ; do 

		sed -e "s/<XXYEARXX>/${cyear}/"  -e "s/<XXVARGRDXX>/${gtype}/"  Sosie_3D_interp_BDYs.slurm.tmp > ./JOBS/Sosie_3D_interp_BDYs_y${cyear}_${gtype}.slurm
		
		qsub ./JOBS/Sosie_3D_interp_BDYs_y${cyear}_${gtype}.slurm

	done
done 
