#!/bin/bash
#PBS -l walltime=01:00:00
#PBS -N CURL
#PBS -M ctalandi@ifremer.fr
set -xv
ulimit -s
ulimit -s unlimited

CONFIG=CREG12.L75
CASE=REF08



if [ ! -d WORK ]  ;  then mkdir WORK ; fi
if [ ! -d ${CASE} ] ;  then mkdir ${CASE} ; fi


cd WORK
ln -sf ../cdfcurl .
ln -sf /data0/project/drakkar/CONFIGS/CREG12.L75/GRID/CREG12.L75-REF08_mesh_hgr.nc mesh_hgr.nc 

#DIR="/home/ctalandi/TOOLS/SSHFS/datarmor-data/${CONFIG}/${CONFIG}-${CASE}-MEAN/1m"
#DIR="/home/ctalandi/TOOLS/SSHFS/drakkarcom/${CONFIG}/${CONFIG}-${CASE}-MEAN/1m"
DIR="/data0/project/drakkar/CONFIGS/CREG12.L75/CREG12.L75-REF08-S/5d/"



c_year=2015
e_year=2015
tag="m07d05.5d"

while [ $c_year -le $e_year ]   ; do 

        ./cdfcurl -u ${DIR}/${c_year}/CREG12.L75-${CASE}_y${c_year}${tag}_gridU.nc uwspd10 -v ${DIR}/${c_year}/CREG12.L75-${CASE}_y${c_year}${tag}_gridV.nc vwspd10 -l 0 -o ../${CASE}/CREG12.L75-${CASE}_y${c_year}${tag}_WS10.nc 
        #./cdfcurl -u ${DIR}/${c_year}/CREG025.L75-${CASE}_y${c_year}.1m_gridU.nc sozotaux -v ${DIR}/${c_year}/CREG025.L75-${CASE}_y${c_year}.1m_gridV.nc sometauy -l 0 -o ../${CASE}/CREG025.L75-${CASE}_y${c_year}.1m_WSCURL.nc 

        let c_year=$c_year+1

done 
