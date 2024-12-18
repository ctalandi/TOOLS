#!/bin/bash

# To launch only when 1d & 1m TKE and EKE for a given year have been produced 

if [ ! -d JOBS ] ; then mkdir JOBS ; fi
if [ ! -d OUT ] ; then mkdir OUT ; fi

EXP=REF08
SYEAR=2014
EYEAR=2011
FREQ="1m 5d"
Elpastime=3600

# Archive TKE & EKE fields
###########################
for cyear in `seq $SYEAR -1 $EYEAR` ; do
	for zfreq in `echo $FREQ` ; do
         	sed -e "s/<XXMYEXPXX>/${EXP}/" \
         	    -e "s/<XXELAPSXX>/${Elpastime}/" \
         	    -e "s/<XXFREQXX>/${zfreq}/" \
         	    -e "s/<XXMYYEAXX>/${cyear}/" do_TarTEKE.bash.tmp > ./JOBS/do_TarTEKE_${zfreq}_${cyear}.bash
         	ccc_msub ./JOBS/do_TarTEKE_${zfreq}_${cyear}.bash
	done

done
