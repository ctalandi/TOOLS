#!/bin/bash


set -xv 

for file in `echo grid2D  gridS  gridT  gridU  gridV`; do 

	for year in `echo 1996 2000 2004 2008 2012 2016 2020 `; do 
		DATAIN=/home1/scratch/ctalandi/PREPOST/SUBTROPGYRE-BDY-OPERATE-NOLEAP/${file}/${year}
		DATAOU=/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/BDYS/SUBTROPGYRE/NOLEAP/${year}
		ncrcat ${DATAIN}/GLORYS12V1-CREG025.L75_SUBTROPGYRE_y${year}.1d_${file}_S1.nc ${DATAIN}/GLORYS12V1-CREG025.L75_SUBTROPGYRE_y${year}.1d_${file}_S2.nc ${DATAOU}/GLORYS12V1-CREG025.L75_SUBTROPGYRE_y${year}.1d_${file}.nc &> loc.out
	done 

done 
