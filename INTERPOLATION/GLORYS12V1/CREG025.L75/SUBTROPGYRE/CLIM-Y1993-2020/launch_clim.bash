#!/bin/bash

set -xv 

SY=1993
EY=2020

do_leap=0
do_clim=1

if [ ! -d JOBS  ] ; then mkdir ./JOBS ; fi 

# Prepare leap years i removing the additionnal day to get only 365 days
if [ $do_leap -eq 1 ] ; then 

	for gtype in `echo gridT gridS gridU gridV grid2D  ` ; do 
	
	       sed -e "s/<XXSYEARXX>/${SY}/g"  \
	           -e "s/<XXEYEARXX>/${EY}/g"  \
  		   -e "s/<XXVARGRDXX>/${gtype}/g"  make_noleap.pbs.tmp > ./JOBS/make_noleap_y${SY}-${EY}_${gtype}.pbs

	       sed -e "s/<XXSYEARXX>/${SY}/g"  \
	           -e "s/<XXEYEARXX>/${EY}/g"  \
  		   -e "s/<XXVARGRDXX>/${gtype}/g"  Job_make_noleap.pbs.tmp > ./JOBS/Job_make_noleap_y${SY}-${EY}_${gtype}.pbs
	       
	       #qsub ./JOBS/Job_make_noleap_y${SY}-${EY}_${gtype}.pbs
	       chmod 750 ./JOBS/Job_make_noleap_y${SY}-${EY}_${gtype}.pbs
	       ./JOBS/Job_make_noleap_y${SY}-${EY}_${gtype}.pbs
	
	done

fi

# Compute the climatology
if [ $do_clim -eq 1 ] ; then 

	for gtype in `echo gridT gridS gridU gridV grid2D ` ; do 
	
	       sed -e "s/<XXSYEARXX>/${SY}/g"  \
	           -e "s/<XXEYEARXX>/${EY}/g"  \
	           -e "s/<XXVARGRDXX>/${gtype}/g"  make_clim.pbs.tmp > ./JOBS/make_clim_y${SY}-${EY}_${gtype}.pbs

	       sed -e "s/<XXSYEARXX>/${SY}/g"  \
	           -e "s/<XXEYEARXX>/${EY}/g"  \
	           -e "s/<XXVARGRDXX>/${gtype}/g"  Job_make_clim.pbs.tmp > ./JOBS/Job_make_clim_y${SY}-${EY}_${gtype}.pbs
	       
	       #qsub ./JOBS/Job_make_clim_y${SY}-${EY}_${gtype}.pbs
	       chmod 750 ./JOBS/Job_make_clim_y${SY}-${EY}_${gtype}.pbs
	       ./JOBS/Job_make_clim_y${SY}-${EY}_${gtype}.pbs
	
	done

fi
