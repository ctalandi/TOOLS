#!/bin/bash
set -xv 

module unload nco/4.6.4_gcc-6.3.0
module load nco/4.7.1_conda
module list

# Apply the right _FillValue on all variables to make the data set coherent 
# Since the GLORYS12V1 data is only interpolated over the vertical for 3D variables, 
# the grid2D and icemod are not concerned by the interpolation step and still have a 
# filled value of 9.96921e+36 , while others have a -9999. value

# To apply only at the end of the full process

S_YEAR=$1
E_YEAR=$2

for year in `seq $S_YEAR $E_YEAR `; do 

	DATAINI=/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/BDYS/BERING/${year}
	DATAOUT=/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/BDYS/BERING/${year}
	WRKAREA=/home1/scratch/ctalandi/PREPOST

	echo $year  

	for gtype in `echo grid2D icemod `; do 

		echo "		$gtype" 
	
		DIR=${WRKAREA}/BDY-OPERATE-FILL/${year}/${gtype}
		if [ ! -d ${DIR} ] ; then mkdir -p ${DIR} ; fi
		cd ${DIR}

        	if [ ${gtype} == 'grid2D' ] ;then
        	        mv ${DATAINI}/GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}.nc  GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp.nc
        	        ncatted -a missing_value,sossheig,d,, GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp.nc GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp1.nc
        	        ncatted -a _FillValue,sossheig,m,d,-9999. GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp1.nc GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}.nc
        	fi

        	if [ ${gtype} == 'icemod' ] ;then
        	        mv ${DATAINI}/GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}.nc  GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp.nc
        	        ncatted -a missing_value,iicethic,d,, GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp.nc GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp1.nc
        	        ncatted -a _FillValue,iicethic,m,d,-9999. GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp1.nc GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp2.nc

        	        ncatted -a missing_value,ileadfra,d,, GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp2.nc GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp3.nc
        	        ncatted -a _FillValue,ileadfra,m,d,-9999. GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp3.nc  GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp4.nc

        	        ncatted -a missing_value,isnowthi,d,, GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp4.nc GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp5.nc
        	        ncatted -a _FillValue,isnowthi,m,d,-9999. GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}_tmp5.nc  GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}.nc
        	fi

		mv GLORYS12V1-CREG12.L75_BERING_y${year}.1d_${gtype}.nc ${DATAOUT}/.
	
	
	done 

done
