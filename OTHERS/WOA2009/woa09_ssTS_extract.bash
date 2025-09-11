#!/bin/bash

set -xv 


ncks -d z,0,0                  woa09_SalAbs_monthly_1deg_SA_CMA_drowned_Ex_L75_SM5.nc     woa09_SAsss01-12_monthly_1deg_SA_CMA_drowned_Ex_L75_SM5.nc
ncwa -O -a z                   woa09_SAsss01-12_monthly_1deg_SA_CMA_drowned_Ex_L75_SM5.nc woa09_SAsss01-12_monthly_1deg_SA_CMA_drowned_Ex_L75_SM5.nc
ncks --mk_rec_dmn time_counter woa09_SAsss01-12_monthly_1deg_SA_CMA_drowned_Ex_L75_SM5.nc woa09_SAsss01-12_monthly_1deg_SA_CMA_drowned_Ex_L75_SM5.nc

ncks -d z,0,0                  woa09_ConTem_monthly_1deg_CT_CMA_drowned_Ex_L75_SM5.nc       woa09_CTsst01-12_monthly_1deg_CT_CMA_drowned_Ex_L75_SM5.nc
ncwa -O -a z                   woa09_CTsst01-12_monthly_1deg_CT_CMA_drowned_Ex_L75_SM5.nc   woa09_CTsst01-12_monthly_1deg_CT_CMA_drowned_Ex_L75_SM5.nc
ncks --mk_rec_dmn time_counter woa09_CTsst01-12_monthly_1deg_CT_CMA_drowned_Ex_L75_SM5.nc   woa09_CTsst01-12_monthly_1deg_CT_CMA_drowned_Ex_L75_SM5.nc

