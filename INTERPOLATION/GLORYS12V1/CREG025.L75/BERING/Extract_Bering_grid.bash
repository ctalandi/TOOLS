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
backward=0


NCKS="ncks"
OPT="-O -F "

if [ ! -d GRID-OPERATE ] ; then mkdir GRID-OPERATE ; fi 

cd GRID-OPERATE


if [ $forward -eq 1 ] ; then 
	# Extract the mesh that will be used to perform the interpolation
	# The target area should be covered by the GLORYS12V1 data set for sure
	# FORTRAN INDICES
	i1=197   ;   i2=228
	j1=592   ;   j2=603
	
	
	ln -sf /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/GRID/CREG025.L75-NEMO420_mesh_mask.nc .
	
	${NCKS} ${OPT} -d x,${i1},${i2} -d y,${j1},${j2} CREG025.L75-NEMO420_mesh_mask.nc  CREG025.L75-NEMO420_mesh_mask_Bering.nc 
	ncpdq -a -x CREG025.L75-NEMO420_mesh_mask_Bering.nc CREG025.L75-NEMO420_mesh_mask_Bering_EWflip.nc 
	ncpdq -a -y CREG025.L75-NEMO420_mesh_mask_Bering_EWflip.nc CREG025.L75-NEMO420_mesh_mask_Bering_Glorys12v1.nc
	
	mv CREG025.L75-NEMO420_mesh_mask_Bering_Glorys12v1.nc /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/GRID/.

	ln -sf /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/GRID/CREG025.L75_domain_cfg.nc .
	
	${NCKS} ${OPT} -d x,${i1},${i2} -d y,${j1},${j2} CREG025.L75_domain_cfg.nc  CREG025.L75_domain_cfg_Bering.nc 
	ncpdq -a -x CREG025.L75_domain_cfg_Bering.nc  CREG025.L75_domain_cfg_Bering_EWflip.nc 
	ncpdq -a -y CREG025.L75_domain_cfg_Bering_EWflip.nc  CREG025.L75-NEMO420_domain_cfg_Bering_Glorys12v1.nc
	
	mv CREG025.L75-NEMO420_domain_cfg_Bering_Glorys12v1.nc /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/GRID/.

fi


if [ $backward -eq 1 ] ; then 

	# Turn back the original grid extration to control data and transport
	#######################################################################
	
	# FORTRAN INDICES
	# T-points
	iT1="18"  ;  iT2="59"
	jT1="2"   ;  jT2="11"
	
	# The following i/j shift against T-point is because all variables extracted are 
	# on the CREG12.L75 original grid that has been reversed to fit the GLORYS12V1 
	# orientation for the interpolation
	# V-points
	iV1="18"  ;  iV2="59"
	jV1="3"   ;  jV2="12"
	
	# U-points
	iU1="18"  ;  iU2="59"
	jU1="2"   ;  jU2="11"
	
	
	fiin=CREG025.L75-NEMO420_mesh_mask.nc
	ftmpT=CREG025.L75-NEMO420_mesh_mask_Bering_Glorys12v1_tmpT.nc 
	ftmpU=CREG025.L75-NEMO420_mesh_mask_Bering_Glorys12v1_tmpU.nc 
	ftmpV=CREG025.L75-NEMO420_mesh_mask_Bering_Glorys12v1_tmpV.nc 
	fout=CREG025.L75-NEMO420_mesh_mask_Bering_Glorys12v1_Tgt.nc 
	
	# Extract the corect data depending the considedred point
	${NCKS} ${OPT} -d x,${iT1},${iT2} -d y,${jT1},${jT2} -v gdept_1d,glamt,gphit,tmask ${fiin} ${ftmpT}
	${NCKS} ${OPT} -d x,${iU1},${iU2} -d y,${jU1},${jU2} -v glamu,gphiu,umask ${fiin} ${ftmpU}
	${NCKS} ${OPT} -d x,${iV1},${iV2} -d y,${jV1},${jV2} -v e3v_0,e1v,glamv,gphiv,vmask ${fiin} ${ftmpV}
	
	# Gather into the same file
	ncks -A ${ftmpU} ${ftmpV}
	ncks -A ${ftmpV} ${ftmpT}
	
	# East-West flip
	ncpdq -a -x ${ftmpT} ${fout}

fi
