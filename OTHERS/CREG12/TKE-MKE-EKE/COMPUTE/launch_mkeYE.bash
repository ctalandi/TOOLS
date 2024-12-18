#!/bin/bash

# To launch only when rebuilt files have been moved from there original place to a new one

if [ ! -d JOBS ] ; then mkdir JOBS ; fi
if [ ! -d OUT ] ; then mkdir OUT ; fi

EXP=REF08
SYEAR=2010
EYEAR=2008
Elpastime=1200

# Upper 510m monthly EKE 
#########################
for cyear in `seq $SYEAR -1 $EYEAR` ; do
         sed -e "s/<XXMYEXPXX>/${EXP}/" \
             -e "s/<XXELAPSXX>/${Elpastime}/" \
             -e "s/<XXMYYEAXX>/${cyear}/" do_mkeYE.bash.tmp > ./JOBS/do_mkeYE_${cyear}.bash
         ccc_msub ./JOBS/do_mkeYE_${cyear}.bash

done
