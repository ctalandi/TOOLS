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


# Rebuild the corresponding Domcfg as mesh_mask files as well 
# for the Bering strait. 
# It relies on the last step FINAL script make_final_Bering_bdys.slurm.tmp

set -xv

NCKS="ncks"
OPT="-O -F "

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


fiin=CREG12.L75-REF09_mesh_mask_Bering_Glorys12v1.nc 
ftmpT=CREG12.L75-REF09_mesh_mask_Bering_Glorys12v1_tmpT.nc 
ftmpU=CREG12.L75-REF09_mesh_mask_Bering_Glorys12v1_tmpU.nc 
ftmpV=CREG12.L75-REF09_mesh_mask_Bering_Glorys12v1_tmpV.nc 
fout=CREG12.L75-REF09_mesh_mask_Bering_Glorys12v1_Tgt.nc 

ln -sf /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/MESH/${fiin} .

# Extract the corect data depending the considedred point
${NCKS} ${OPT} -d x,${iT1},${iT2} -d y,${jT1},${jT2} -v gdept_1d,glamt,gphit,tmask ${fiin} ${ftmpT}
${NCKS} ${OPT} -d x,${iU1},${iU2} -d y,${jU1},${jU2} -v glamu,gphiu,umask ${fiin} ${ftmpU}
${NCKS} ${OPT} -d x,${iV1},${iV2} -d y,${jV1},${jV2} -v e3v_0,e1v,glamv,gphiv,vmask ${fiin} ${ftmpV}

# Gather into the same file
ncks -A ${ftmpU} ${ftmpV}
ncks -A ${ftmpV} ${ftmpT}

# East-West flip
ncpdq -a -x ${ftmpT} ${fout}

