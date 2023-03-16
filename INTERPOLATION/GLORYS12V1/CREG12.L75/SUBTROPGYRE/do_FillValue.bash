#!/bin/bash
set -x 

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

	DATAINI=/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/BDYS/SUBTROPGYRE/${year}
	DATAOUT=/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/BDYS/SUBTROPGYRE/${year}
	WRKAREA=/home1/scratch/ctalandi/PREPOST

	echo $year  

	for gtype in `echo grid2D `; do 

		echo "		$gtype" 
	
		DIR=${WRKAREA}/BDY-OPERATE-FILL/${year}/${gtype}
		if [ ! -d ${DIR} ] ; then mkdir -p ${DIR} ; fi
		cd ${DIR}

        	if [ ${gtype} == 'grid2D' ] ;then
        	        mv ${DATAINI}/GLORYS12V1-CREG12.L75_SUBTROPGYRE_y${year}.1d_${gtype}.nc  GLORYS12V1-CREG12.L75_SUBTROPGYRE_y${year}.1d_${gtype}_tmp.nc
        	        ncatted -a missing_value,sossheig,d,, GLORYS12V1-CREG12.L75_SUBTROPGYRE_y${year}.1d_${gtype}_tmp.nc GLORYS12V1-CREG12.L75_SUBTROPGYRE_y${year}.1d_${gtype}_tmp1.nc
        	        ncatted -a _FillValue,sossheig,m,d,-9999. GLORYS12V1-CREG12.L75_SUBTROPGYRE_y${year}.1d_${gtype}_tmp1.nc GLORYS12V1-CREG12.L75_SUBTROPGYRE_y${year}.1d_${gtype}.nc
        	fi

		mv GLORYS12V1-CREG12.L75_SUBTROPGYRE_y${year}.1d_${gtype}.nc ${DATAOUT}/.
	
	
	done 

done
