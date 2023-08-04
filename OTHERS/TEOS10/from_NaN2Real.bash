#/bin/bash 

set -xv 

AREA=BERING

for year in `seq 1994 2020`; do 

	cd ${year}

	for var in `echo CT SA`; do 
		mv GLORYS12V1-CREG12.L75_${AREA}_y${year}.1d_grid${var}.nc GLORYS12V1-CREG12.L75_${AREA}_y${year}.1d_grid${var}.nc_NaN
		ncatted -a _FillValue,${var},o,f,-9999.  GLORYS12V1-CREG12.L75_${AREA}_y${year}.1d_grid${var}.nc_NaN GLORYS12V1-CREG12.L75_${AREA}_y${year}.1d_grid${var}.nc
	done 

	cd ../

done 
