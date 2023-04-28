#!/bin/bash
#SBATCH -J weights
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=24
#SBATCH --time=2:00:00
#SBATCH -e out_weights.e%j
#SBATCH -o out_weights.o%j
#SBATCH --exclusive
 set -x

cd /home1/datawork/ctalandi/PRE-POST/FREDY/WEIGHTS/OFF-LINE/PIOMAS

############ ENV ############
BINDIR=/home1/datawork/ctalandi/WTOOLS/tools/WEIGHTS
#BINDIR=/home1/datahome/ctalandi/DEV/GITREP/DCM_4.0/DCMTOOLS/NEMOREF/NEMO4.0.1/tools/WEIGHTS
set -xv
#############################

#CONFIG=CREG025.L75
CONFIG=CREG12.L75
#INTERP_TYPE=bicubic
INTERP_TYPE=bilinear

#FORG=era5
FORG=piomas
#FORG=dfs5.2

# Interpolation type: bilin/bicub
##################################
SHORT_INTERP=$( echo $INTERP_TYPE | cut -c 1-5 )

# SCRIP Weight file name 
##################################
SCRIP_WGTFILE=data_nemo_${SHORT_INTERP}_${CONFIG}.nc

# NEMO Weight file name 
##################################
NEMO_WGTFILE=reshape_${CONFIG}_${INTERP_TYPE}.nc

ulimit -S -s unlimited
#gdb ${BINDIR}/scripgrid.exe 
#valgrind --track-origins=yes --main-stacksize=150000000  --max-stackframe=12000000 ${BINDIR}/scripgrid.exe 

unit='m' # Default units for both snow and heff

for year in `seq 1980 1981 `; do 
	for var in `echo heff snow area `; do 

		if [ ${var} == 'area' ] ; then unit='-' ; fi 

		sed -e "s/<XXYEARXX>/$year/"  \
		    -e "s/<XXUNITXX>/$unit/"  \
		    -e "s/<XXVARXX>/${var}/" namelist_${SHORT_INTERP}_${FORG}_${CONFIG}.tmp  > namelist_${SHORT_INTERP}_${FORG}_${CONFIG}_${var}
		
		time ${BINDIR}/scripinterp.exe namelist_${SHORT_INTERP}_${FORG}_${CONFIG}_${var} 

	done 
done 

