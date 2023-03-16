#!/bin/bash
#set -xv 

S_YEAR=$1
E_YEAR=$2

for year in `seq $S_YEAR $E_YEAR `; do 

	DATAOUT="/home1/datawork/ctalandi/PRE-POST/FREDY/BUILD-BDYS/CREG12.L75/BERING/INTERP/${year}"
	echo $year  

	for gtype in `echo gridT gridS gridU gridV`; do 

		echo "		$gtype" 
	
		DIR="./OPERATE/${year}/${gtype}"
		if [ ${gtype} == 'gridT' ] ;then 
			ncap2 -s "where(votemper == 50.) votemper=0." ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}_tmp.nc  ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}.nc
			ncatted -a missing_value,votemper,c,f,0. ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}.nc
		fi
		if [ ${gtype} == 'gridS' ] ;then 
			ncap2 -s "where(vosaline == 40.) vosaline=0." ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}_tmp.nc  ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}.nc
			ncatted -a missing_value,vosaline,c,f,0. ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}.nc
		fi
		if [ ${gtype} == 'gridU' ] ;then 
			ncap2 -s "where(vozocrtx == 10.) vozocrtx=0." ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}_tmp.nc  ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}.nc
			ncatted -a missing_value,vozocrtx,c,f,0. ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}.nc
		fi
		if [ ${gtype} == 'gridV' ] ;then 
			ncap2 -s "where(vomecrty == 10.) vomecrty=0." ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}_tmp.nc  ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}.nc
			ncatted -a missing_value,vomecrty,c,f,0. ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}.nc
		fi
		mv ${DIR}/GLORYS12V1-CREG12.L75_y${year}.1d_${gtype}.nc ${DATAOUT}/.
	
	
	done 

done
