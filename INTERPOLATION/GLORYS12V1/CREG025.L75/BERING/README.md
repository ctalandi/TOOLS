## Scripts used to perform the vertical interpolation of GLORYS12V1 data set onto the CREG025.L75 grid for the NEMO420 experiment suite <br>
>
> The current scripts used are located there /home1/datawork/ctalandi/PRE-POST/FREDY/BUILD-BDYS/CREG025.L75/BERING <br>
> The interpolation relies o the Sosie tools /home1/datahome/ctalandi/DEV/SOSIE_GIT_MASTER/bin/sosie3.x <br> 
> The weight files have been already defined sosie_mapping_GLORYS12V1-CREG025.L75_T.nc, sosie_mapping_GLORYS12V1-CREG025.L75_U.nc sosie_mapping_GLORYS12V1-CREG025.L75_V.nc <br>
> The main script is launch_Sosie.bash, just set the years over which to perform the interpolation <br>
> After this step, since the _FillValue_ is correctly set after the interpolation, the scrip do_misval.bash will just move files <br>
> Then to finalise need to extract, flip and change velocoties sign under the FINAL directory <br>
> The final directory where are stored the data is /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/BDYS/BERING <br> 

Then a final step is required to make the interpolated data ready to be used by CREG12.L75 configuration. This step is launch (interactively) in the FINAL directory using launch.bash script. 

### Few steps:
- perform the interpolation 
- Finalise the data:
  - extract the correct sub-domain
  - East-West flip 
  - change velocities sign
