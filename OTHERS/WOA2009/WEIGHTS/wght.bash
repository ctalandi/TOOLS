#!/bin/bash
#SBATCH -J weights
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=24
#SBATCH --constraint=HSW24
#SBATCH --time=0:10:00
#SBATCH -e out_weights.e%j
#SBATCH -o out_weights.o%j
#SBATCH --exclusive
 set -x

cd /scratch/cnt0028/lpo7420/verena/CREG12.L75/TOOLS/convert_orca12_to_creg12/WEIGHTS/INIT-STATE/WOA09

############ ENV ############
BINDIR=/scratch/cnt0028/lpo7420/talandic/NEMODRAK/NEMODRAK_3.6_STABLE_HEAD/NEMOREF/NEMOGCM/TOOLS/WEIGHTS/
set -xv
#############################

CONFIG=CREG12.L75
RESOL=HR
#INTERP_TYPE=bicubic
INTERP_TYPE=bilinear

# Interpolation type: bilin/bicub
##################################
SHORT_INTERP=$( echo $INTERP_TYPE | cut -c 1-5 )

# SCRIP Weight file name 
##################################
SCRIP_WGTFILE=data_woa2009_${SHORT_INTERP}_${CONFIG}_${RESOL}.nc

# NEMO Weight file name 
##################################
NEMO_WGTFILE=reshape_${CONFIG}_${INTERP_TYPE}_${RESOL}.nc

ulimit -S -s unlimited
#gdb ${BINDIR}/scripgrid.exe 
#valgrind --track-origins=yes --main-stacksize=150000000  --max-stackframe=12000000 ${BINDIR}/scripgrid.exe 


#${BINDIR}/scripgrid.exe 
${BINDIR}/scripgrid.exe namelist_reshape_${SHORT_INTERP}_${RESOL}
${BINDIR}/scrip.exe namelist_reshape_${SHORT_INTERP}_${RESOL}
${BINDIR}/scripshape.exe namelist_reshape_${SHORT_INTERP}_${RESOL}
#mv data_nemo_${SHORT_INTERP}_${RESOL}.nc ../${SCRIP_WGTFILE}
#mv ${NEMO_WGTFILE} ..

