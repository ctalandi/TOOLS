#!/bin/bash

set -xv 

SY=2013
EY=2020

for cyear in `seq $SY $EY ` ; do 

	for gtype in `echo gridT gridS gridU gridV grid2D ` ; do 

		sed -e "s/<XXYEARXX>/${cyear}/g"  -e "s/<XXVARGRDXX>/${gtype}/g"  Sosie_3D_interp_BDYs.slurm.tmp > ./JOBS/Sosie_3D_interp_BDYs_y${cyear}_${gtype}.slurm
		sed -e "s/<XXYEARXX>/${cyear}/g"  -e "s/<XXVARGRDXX>/${gtype}/g"  Job_Sosie_3D_interp_BDYs.slurm.tmp > ./JOBS/Job_Sosie_3D_interp_BDYs_y${cyear}_${gtype}.slurm
		
		qsub ./JOBS/Job_Sosie_3D_interp_BDYs_y${cyear}_${gtype}.slurm

	done
done 
