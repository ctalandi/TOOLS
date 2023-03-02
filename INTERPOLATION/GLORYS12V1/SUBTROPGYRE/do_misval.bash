#!/bin/bash
set -x 

S_YEAR=$1
E_YEAR=$2
area=SUBTROPGYRE

for year in `seq $S_YEAR $E_YEAR `; do 

	DATAOUT="/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/BDYS/${area}/${year}"
	if [ ! -d ${DATAOUT} ] ; then mkdir -p ${DATAOUT} ; fi

	echo $year  

	for gtype in `echo gridT gridS gridU gridV`; do 

		echo "		$gtype" 
	
		DIR="/home1/scratch/ctalandi/PREPOST/OPERATE-INTERP/${year}/${gtype}"
# Finally, the following lines might not be necessary since the _FillValue is already there after the interpolation
#	  DIR="./OPERATE/${year}/${gtype}"
#		if [ ${gtype} == 'gridT' ] ;then 
#			ncap2 -s "where(votemper == 40.) votemper=0." ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}_tmp.nc  ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}.nc
#			ncatted -a missing_value,votemper,c,f,0. ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}.nc
#		fi
#		if [ ${gtype} == 'gridS' ] ;then 
#			ncap2 -s "where(vosaline == 50.) vosaline=0." ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}_tmp.nc  ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}.nc
#			ncatted -a missing_value,vosaline,c,f,0. ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}.nc
#		fi
#		if [ ${gtype} == 'gridU' ] ;then 
#			ncap2 -s "where(vozocrtx == 10.) vozocrtx=0." ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}_tmp.nc  ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}.nc
#			ncatted -a missing_value,vozocrtx,c,f,0. ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}.nc
#		fi
#		if [ ${gtype} == 'gridV' ] ;then 
#			ncap2 -s "where(vomecrty == 10.) vomecrty=0." ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}_tmp.nc  ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}.nc
#			ncatted -a missing_value,vomecrty,c,f,0. ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}.nc
#		fi
#		mv ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}.nc ${DATAOUT}/.
		mv ${DIR}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}_tmp.nc ${DATAOUT}/GLORYS12V1-CREG12.L75_${area}_y${year}.1d_${gtype}.nc
	
	
	done 

done
