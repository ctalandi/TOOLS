#!/bin/bash

# To launch only when rebuilt files have been moved from there original place to a new one

if [ ! -d JOBS ] ; then mkdir JOBS ; fi
if [ ! -d OUT ] ; then mkdir OUT ; fi

EXP=REF08
SYEAR=2014
EYEAR=2008
Elpastime=64800

# High frequency EKE 
#########################
for cyear in `seq $SYEAR -1 $EYEAR` ; do
    for month in `seq 1 12` ; do
         sed -e "s/<XXMONTHXX>/${month}/" \
             -e "s/<XXMYEXPXX>/${EXP}/" \
             -e "s/<XXELAPSXX>/${Elpastime}/" \
             -e "s/<XXMYYEAXX>/${cyear}/" do_tkeMO.bash.tmp > ./JOBS/do_tkeMO_${cyear}m${month}.bash
         ccc_msub ./JOBS/do_tkeMO_${cyear}m${month}.bash

    done
done
