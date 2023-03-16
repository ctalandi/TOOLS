#!/bin/bash
set -xv 

S_YEAR=$1
E_YEAR=$2

for year in `seq $S_YEAR $E_YEAR `; do 

	DATAOUT="/home1/datawork/ctalandi/PRE-POST/FREDY/BUILD-BDYS/CREG025.L75/BERING/INTERP/${year}"
	WRKAREA=/home1/scratch/ctalandi/PREPOST
	if [ ! -d ${DATAOUT} ] ; then mkdir ${DATAOUT} ; fi 

	echo $year  

	for gtype in `echo gridT gridS gridU gridV grid2D icemod`; do 

		echo "		$gtype" 
	
		DIR=${WRKAREA}/BERING-OPERATE-INTERP/${year}/${gtype}
		mv ${DIR}/GLORYS12V1-CREG025.L75_y${year}.1d_${gtype}_tmp.nc ${DATAOUT}/GLORYS12V1-CREG025.L75_y${year}.1d_${gtype}.nc 
	
	
	done 

done
