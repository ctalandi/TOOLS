#!/bin/bash
######PBS -l mem=115g
#PBS -e ./JOBS/bdys_<XXYEARXX>_<XXVARGRDXX>_ext.err
#PBS -o ./JOBS/bdys_<XXYEARXX>_<XXVARGRDXX>_ext.out
#PBS -l walltime=00:30:00
#PBS -N BerEx_<XXYEARXX>_<XXVARGRDXX>
#PBS -m n
#
ulimit -s unlimited
source /usr/share/Modules/3.2.10/init/bash
#module load NETCDF-test/4.3.3.1-impi-intel2018
module load nco/4.6.4_gcc-6.3.0


set -xv



forward=1


NCKS="ncks"
OPT="-O -F "

if [ ! -d GRID-OPERATE ] ; then mkdir GRID-OPERATE ; fi 

cd GRID-OPERATE


if [ $forward -eq 1 ] ; then 
	# Extract the mesh that will be used to perform the interpolation
	# The target area should be covered by the GLORYS12V1 data set for sure
	# FORTRAN INDICES
	i1=47    ;   i2=334
	j1=1     ;   j2=15
	
	
	# Mesh mask 
	ln -sf /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/GRID/CREG025.L75-NEMO420_mesh_mask.nc .
	${NCKS} ${OPT} -d x,${i1},${i2} -d y,${j1},${j2} CREG025.L75-NEMO420_mesh_mask.nc  CREG025.L75-NEMO420_mesh_mask_Subtropgyre_Glorys12v1.nc 
	mv CREG025.L75-NEMO420_mesh_mask_Subtropgyre_Glorys12v1.nc /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/GRID/.

	# Domain config (for geographical coordinates that are clean
	ln -sf /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/GRID/CREG025.L75_domain_cfg.nc .
	${NCKS} ${OPT} -d x,${i1},${i2} -d y,${j1},${j2} CREG025.L75_domain_cfg.nc  CREG025.L75-NEMO420_domain_cfg_Subtropgyre_Glorys12v1.nc 
	mv CREG025.L75-NEMO420_domain_cfg_Subtropgyre_Glorys12v1.nc /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/GRID/.

fi
