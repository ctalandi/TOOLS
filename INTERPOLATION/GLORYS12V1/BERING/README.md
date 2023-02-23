## Scripts used to perform the vertical interpolation of GLORYS12V1 data set onto the CREG12.L75 grid for the REF09 experiment<br>
>
> The current scripts used are located there /home1/datawork/ctalandi/PRE-POST/FREDY/BUILD-BDYS/CREG12.L75/BERING <br>
> The interpolation relies o the Sosie tools /home1/datahome/ctalandi/DEV/SOSIE_GIT_MASTER/bin/sosie3.x <br> 
> The weight files have been already defined sosie_mapping_GLORYS12V1-CREG12.L75_T.nc, sosie_mapping_GLORYS12V1-CREG12.L75_U.nc sosie_mapping_GLORYS12V1-CREG12.L75_V.nc <br>
> The main script is launch.bash, just set the years over which to perform the interpolation <br>
> After this step, we have to set the land grid points to zero in using the scrip do_misval.bash <br>
> The finla directory where are stored the data is /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/BDYS/BERING <br> 
