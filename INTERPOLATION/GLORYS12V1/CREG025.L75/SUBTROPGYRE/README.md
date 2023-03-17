## Scripts used to perform the vertical interpolation of GLORYS12V1 data set onto the CREG025.L75 grid for the NEMO420 experiment suite <br>
>
> The current scripts used are located there /home1/datawork/ctalandi/PRE-POST/FREDY/BUILD-BDYS/CREG025.L75/SUBTROPGYRE <br>
> The interpolation relies o the Sosie tools /home1/datahome/ctalandi/DEV/SOSIE_GIT_MASTER/bin/sosie3.x <br> 
> The weight files have been already defined sosie_mapping_GLORYS12V1-CREG025.L75_T.nc, sosie_mapping_GLORYS12V1-CREG025.L75_U.nc sosie_mapping_GLORYS12V1-CREG025.L75_V.nc <br>
> The main script is launch_Sosie.bash, just set the years over which to perform the interpolation <br>
> Then to finalise need to extract the correct sub-domain the FINAL directory with the Job_finalise.slurm.tmp job<br>
> The final directory where are stored the data is /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/BDYS/SUBTROPGYRE <br> 

### Few steps:
- perform the interpolation 
- Finalise the data:
  - extract the correct sub-domain
