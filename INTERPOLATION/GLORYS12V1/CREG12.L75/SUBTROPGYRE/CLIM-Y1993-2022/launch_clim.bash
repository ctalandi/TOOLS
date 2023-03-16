#!/bin/bash

set -xv 

SY=1993
EY=2022

do_leap=0
do_clim=1

if [ ! -d JOBS  ] ; then mkdir ./JOBS ; fi 

# Prepare leap years i removing the additionnal day to get only 365 days
if [ $do_leap -eq 1 ] ; then 

	for gtype in `echo gridT gridS gridU gridV grid2D ` ; do 
	
	       sed -e "s/<XXSYEARXX>/${SY}/"  \
	           -e "s/<XXEYEARXX>/${EY}/"  \
  		   -e "s/<XXVARGRDXX>/${gtype}/"  make_noleap.pbs.tmp > ./JOBS/make_noleap_y${SY}-${EY}_${gtype}.pbs
	       
	       #qsub ./JOBS/make_noleap_y${SY}-${EY}_${gtype}.pbs
               chmod 750 ./JOBS/make_noleap_y${SY}-${EY}_${gtype}.pbs
	       ./JOBS/make_noleap_y${SY}-${EY}_${gtype}.pbs
	
	done

fi

# Compute the climatology
if [ $do_clim -eq 1 ] ; then 

	for gtype in `echo gridT gridS gridU gridV grid2D ` ; do 
	
	       sed -e "s/<XXSYEARXX>/${SY}/"  \
	           -e "s/<XXEYEARXX>/${EY}/"  \
	           -e "s/<XXVARGRDXX>/${gtype}/"  make_clim.pbs.tmp > ./JOBS/make_clim_y${SY}-${EY}_${gtype}.pbs
	       
	       qsub ./JOBS/make_clim_y${SY}-${EY}_${gtype}.pbs
	
	done

fi
