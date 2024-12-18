#!/bin/bash

# To launch only when rebuilt files have been moved from there original place to a new one

if [ ! -d JOBS ] ; then mkdir JOBS ; fi
if [ ! -d OUT ] ; then mkdir OUT ; fi

EXP=DELTA
SYEAR=2014
EYEAR=2011
Elpastime=7200

# yearly mean 
#############
for cyear in `seq $SYEAR -1 $EYEAR` ; do
         sed -e "s/<XXMYEXPXX>/${EXP}/" \
             -e "s/<XXELAPSXX>/${Elpastime}/" \
             -e "s/<XXMYYEAXX>/${cyear}/" do_YearMean.bash.tmp > ./JOBS/do_YearMean_${cyear}.bash
         ccc_msub ./JOBS/do_YearMean_${cyear}.bash

done
