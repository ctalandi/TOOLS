#!/bin/bash
set -x 

S_YEAR=1994
E_YEAR=2020
area=SUBTROPGYRE

i1=7    ;    i2=277
j1=1    ;    j2=10

for year in `seq $S_YEAR $E_YEAR `; do 

	DATAOUT="/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/BDYS/${area}/${year}"
	if [ ! -d ${DATAOUT} ] ; then mkdir -p ${DATAOUT} ; fi

	echo $year  

	for gtype in `echo gridT gridS gridU gridV grid2D`; do 

		echo "		$gtype" 
	
		DIR="/home1/scratch/ctalandi/PREPOST/SUBTROP-OPERATE-INTERP/${year}/${gtype}"
		ncks -d x,${i1},${i2} -d y,${j1},${j2} ${DIR}/GLORYS12V1-CREG025.L75_${area}_y${year}.1d_${gtype}_tmp.nc ${DATAOUT}/GLORYS12V1-CREG025.L75_${area}_y${year}.1d_${gtype}.nc
	
	
	done 

done

