# Scripts used to donwload either BERING or SUBTROGYRE or SUBPOLARGYRE sub-area<br>
>
> The current scripts used are located there /home1/datawork/ctalandi/PRE-POST/MERCATOR/MIO-GLORYS-DATA<br>

## 4 requirements for that: <br>
1. have an OpenDap access open <br>
2. have a python3 environment (to install once for all, look at env_Glorys12v1)<br>
3. do that on Datarmor through FTP batch session <br>
4. Set an unlimited time record which is required to perform the interpolation using SOSIE (UNLIM-TIME)

NB: The process might be quite long with Time out, need to relaunch several times the jobs before getting the data<br>

### To get full years: <br>
The list of scripts to be used has been simplified:  <br>
find_indexes.py   > To find correct indices of the subdomain to extract <br>
get_glorys12v1_monthly.py > script to extract data by month since it's faisable from remote <br>
get_glorys12v1_daily.py > script to extract data by day because it's too big to extract by month <br>
get_glorys12v1_grid.py > To get the corresponding grid files <br>

launch_getGlorysData.bash > main script to launch the process over few years on a selected area <br>
FTPbatch_jobs_full.pbs.tmp > The Job that will be prepared the script before. <br>

#### The workflow is : <br>
In launch_getGlorysData.bash, set the years to cover and the area & the grid type to process: <br>
```
SYEAR=2021
EYEAR=2022

#EFFDOM="BER"   ;  SAREA=B    # For the Bering strait
EFFDOM="SPG"    ;  SAREA=G    # For the SEDNA BDYs
#EFFDOM="STG"   ;  SAREA=T    # For the CREG southern BDY

FULLLST="grd2D grdTT grdSS grdUU grdVV grdIC"
```
> ./launch_getGlorysData.bash <br>

To check that data set time records are complete, use the do_ctrl.bash script either under that will list all missing tags <br>
/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/INIT/SUBTROPGYRE <br>
or <br>
/home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/INIT/BERING <br>
A report is done for 1 specified year <br>

### To get specific dates : <br>
FTPbatch_jobs_snap.pbs <br>
get_glorys12v1_daily_snap.py > set the tag list by hand in this script and specify if it's to get a monthly file <br>
> qsub FTPbatch_jobs_snap.pbs

### Set an unlimited time record: 
Since few problems occur when submitting a job, this is done in an interactive way. <br>
It is done from there: /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/MERCATOR/GLORYS12V1/INIT/UNLIM-TIME <br>
It relies on the  *ncks -O --mk_rec_dmn time_counter ....* NCO command 


