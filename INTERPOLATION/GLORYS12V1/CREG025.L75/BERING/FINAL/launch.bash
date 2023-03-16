#!/bin/bash

set -xv 

SY=2000
EY=2020


if [ ! -d JOBS ] ; then mkdir -p JOBS  ; fi

for cyear in `seq $SY $EY ` ; do 

	for gtype in `echo gridT gridS gridU gridV grid2D icemod` ; do 

		sed -e "s/<XXYEARXX>/${cyear}/"  -e "s/<XXVARGRDXX>/${gtype}/"  make_final_Bering_bdys.slurm.tmp > ./JOBS/make_final_Bering_bdys_y${cyear}_${gtype}.slurm
		
		# Must be submitted interactivelyy else it crashes (NCO command)
                chmod 750 ./JOBS/make_final_Bering_bdys_y${cyear}_${gtype}.slurm
		./JOBS/make_final_Bering_bdys_y${cyear}_${gtype}.slurm

		#qsub ./JOBS/make_final_Bering_bdys_y${cyear}_${gtype}.slurm

	done
done 
