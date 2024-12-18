#!/bin/bash

# To launch only when EKE files have been produced 

if [ ! -d JOBS ] ; then mkdir JOBS ; fi
if [ ! -d OUT ] ; then mkdir OUT ; fi

EXP=REF08
SYEAR=2008
EYEAR=2015
Elpastime=1200

# Archive EKE fields
#####################################
sed -e "s/<XXMYEXPXX>/${EXP}/" \
    -e "s/<XXELAPSXX>/${Elpastime}/" \
    -e "s/<XXMSYEAXX>/${SYEAR}/" \
    -e "s/<XXMEYEAXX>/${EYEAR}/" do_TarMKE-YE.bash.tmp > ./JOBS/do_TarMKE-YE_${SYEAR}${EYEAR}.bash
ccc_msub ./JOBS/do_TarMKE-YE_${SYEAR}${EYEAR}.bash

