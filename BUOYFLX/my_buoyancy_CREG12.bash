#!/bin/bash

#set -xv 


dirin='/data0/project/drakkar/CONFIGS/CREG12.L75/CREG12.L75-REF08-S/5d'
dirout='/net/5lpo154/export/drakkar-h3/drakkar/USERS/ctalandi/RES-TEMP/REF08-BUOY'


cdfdir='/home/ctalandi/PREPOST/BUOY/CDF-BUOY/bin'



s_year=2011
e_year=2014

for year in `seq ${s_year} ${e_year}` ; do 

	echo ${year}
	if [ ! -d ${dirout}/${year} ]  ;  then mkdir ${dirout}/${year} ; fi 
	
	# List the number of 5d mean to treat
	taglist=''
	for tfile in `ls ${dirin}/${year}/CREG12.L75-REF08_y????m??d??.5d_gridT.nc` ; do 
		ftype=`basename $tfile`
		interone=`echo $ftype | awk -F_ '{print $2}' `   ; intertwo=${interone%.5d}
		taglist="$taglist ${intertwo:5:10}"
	done 
	
	# Compute the diag.
	for tag in `echo $taglist `; do 
	
		echo $tag 
	      	${cdfdir}/my_cdfbuoyflx_new -t ${dirin}/${year}/CREG12.L75-REF08_y${year}${tag}.5d_gridT.nc -f ${dirin}/${year}/CREG12.L75-REF08_y${year}${tag}.5d_flxT.nc -short 
	      	mv buoyflx.nc  ${dirout}/${year}/CREG12.L75-REF08_y${year}${tag}.5d_buoyflx.nc
	
	done

done
