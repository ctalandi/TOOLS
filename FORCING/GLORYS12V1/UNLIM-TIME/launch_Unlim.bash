#!/bin/bash

set -xv 

SY=2022
EY=2022

msbdm=STG # To treat SUBTROPGYRE data
#msbdm=BER # To treat BERING data

if [ ! -d JOBS ] ; then mkdir JOBS ; fi 

for cyear in `seq $SY $EY ` ; do 

	for gtype in `echo gridT gridS gridU gridV grid2D ` ; do 
	#for gtype in `echo gridT gridS gridU gridV grid2D icemod ` ; do 
		
		shortvar=N
		if [ ${gtype} == "gridT" ] ; then  shortvar=T ;
		elif [ ${gtype} == "gridS" ] ; then  shortvar=S ; 
		elif [ ${gtype} == "gridU" ] ; then  shortvar=U ; 
		elif [ ${gtype} == "gridV" ] ; then  shortvar=V ;
		elif [ ${gtype} == "grid2D" ] ; then  shortvar=D ;
		elif [ ${gtype} == "icemod" ] ; then  shortvar=I ;
		fi

		sed -e "s/<XXYEARXX>/${cyear}/"  \
                    -e "s/<XXSBDMXX>/${msbdm}/"  \
                    -e "s/<XXSHVARXX>/${shortvar}/"  \
                    -e "s/<XXVARGRDXX>/${gtype}/"  make_Unlim.bash.tmp > ./JOBS/make_Unlim_y${cyear}_${gtype}.slurm
		
		qsub ./JOBS/make_Unlim_y${cyear}_${gtype}.slurm

	done
done 
