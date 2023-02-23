#!/bin/bash 

set -x 

SYEAR=2019
EYEAR=2019

#EFFDOM="BER"   ;  SAREA=B  
#EFFDOM="SPG"   ;  SAREA=G       # For SEDNA i.e. over the SPG
EFFDOM="STG"   ;  SAREA=T      # Should called STG since it covers the subtropics 

FULLLST=" grdVV"
FULLLST="grdSS grdUU "
#FULLLST="grd2D grdTT grdSS grdUU "
#FULLLST="grd2D grdTT grdSS grdUU grdVV "
if [ $EFFDOM == "BER" ] ; then FULLLST="grd2D grdTT grdSS grdUU grdVV grdIC"  ; fi 

if [ ! -d ./JOBS ] ; then mkdir JOBS ; fi 

for CYEAR in `seq -w $SYEAR $EYEAR `; do 

	for TYP in `echo ${FULLLST} ` ; do  
	
		sed -e "s/<XXDAREAXX>/$EFFDOM/g"  \
	            -e "s/<XXSHAREXX>/$SAREA/g"   \
	            -e "s/<XXFTYPEXX>/$TYP/g"     \
	            -e "s/<XXCYEARXX>/$CYEAR/g"  FTPbatch_jobs_full.pbs.tmp > ./JOBS/FTPbatch_jobs_full_${EFFDOM}_y${CYEAR}_${TYP}.pbs
		cd ./JOBS 
                qsub FTPbatch_jobs_full_${EFFDOM}_y${CYEAR}_${TYP}.pbs
		cd ../
	
	done

done
