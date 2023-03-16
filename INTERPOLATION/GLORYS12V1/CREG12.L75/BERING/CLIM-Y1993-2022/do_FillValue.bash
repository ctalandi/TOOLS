#!/bin/bash
set -x

module unload nco/4.6.4_gcc-6.3.0 
module load nco/4.7.1_conda
module list

DATAINI=/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/BDYS/BERING/CLIM-Y1993-2022
DATAOUT=/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/BDYS/BERING/CLIM-Y1993-2022

for gtype in `echo gridT gridS gridU gridV icemod grid2D `; do 

	echo "		$gtype" 

	DIR=./OPERATE-FILL/${gtype}
	if [ ! -d ${DIR} ] ; then mkdir -p ${DIR} ; fi 
	cd ${DIR}

	if [ ${gtype} == 'gridT' ] ;then 
	        mv ${DATAINI}/GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc  GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc 
		ncap2 -s "where(votemper >= 49.) votemper=-9999." GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc
	fi
	if [ ${gtype} == 'gridS' ] ;then 
	        mv ${DATAINI}/GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc  GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc 
		ncap2 -s "where(vosaline >= 39.) vosaline=-9999." GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc
	fi

	if [ ${gtype} == 'gridU' ] ;then 
	        mv ${DATAINI}/GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc  GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc 
		ncap2 -s "where(vozocrtx > 1e+09) vozocrtx=-9999." GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc
	fi

	if [ ${gtype} == 'gridV' ] ;then 
	        mv ${DATAINI}/GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc  GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc
		ncap2 -s "where(vomecrty > 1e+09) vomecrty=-9999." GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc
	fi

	if [ ${gtype} == 'grid2D' ] ;then 
	        mv ${DATAINI}/GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc  GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc
		ncatted -a missing_value,sossheig,d,, GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp1.nc 
		ncatted -a _FillValue,sossheig,m,d,-9999. GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp1.nc GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc
	fi

	if [ ${gtype} == 'icemod' ] ;then 
	        mv ${DATAINI}/GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc  GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc
		ncatted -a missing_value,iicethic,d,, GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp.nc GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp1.nc 
		ncatted -a _FillValue,iicethic,m,d,-9999. GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp1.nc GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp2.nc 

		ncatted -a missing_value,ileadfra,d,, GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp2.nc GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp3.nc 
		ncatted -a _FillValue,ileadfra,m,d,-9999. GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp3.nc  GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp4.nc 

		ncatted -a missing_value,isnowthi,d,, GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp4.nc GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp5.nc 
		ncatted -a _FillValue,isnowthi,m,d,-9999. GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}_tmp5.nc  GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc
	fi

	mv GLORYS12V1-CREG12.L75_BERING_CLIM-1993-2022.1d_${gtype}.nc  ${DATAOUT}/.
 
	cd ../../

done 

