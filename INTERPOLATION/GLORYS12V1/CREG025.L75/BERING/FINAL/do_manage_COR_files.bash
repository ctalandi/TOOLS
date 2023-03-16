#!/bin/bash

set -xv 

SYEAR=1993
EYEAR=2020

cd /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/BDYS/BERING

for year in `seq ${SYEAR} ${EYEAR} `; do 
	echo $year ; 
	cd $year ; mkdir NO-COR ; mv GLORYS12V1-CREG025.L75_BERING_y${year}.1d_gridV.nc ./NO-COR/. ; 
	ln -sf GLORYS12V1-CREG025.L75_BERING-COR_y${year}.1d_gridV.nc GLORYS12V1-CREG025.L75_BERING_y${year}.1d_gridV.nc ; 
	cd ../ ; 
done
