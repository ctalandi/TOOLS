## Scripts used to perform the meridional velocity correction to get closer to about 1Sv against Obs<br>
>
> The current scripts used are located there /home1/datahome/ctalandi/DEV/FREDY/CONFIGS/CREG025.L75/GLORYS12V1-BDYS-Y19932022/BERING <br>
> The notebook Glorys12v1_BERING_BDYs_4CREG025.L75_y19932022.ipynb is used from the Datarmor interface<br> 
> Before, an extraction (to get the good orientation) of the grid used for the interpolation is required, use the Extract_Bering_grid.bash script for that, a file called CREG025.L75-NEMO420_mesh_mask_Bering_Glorys12v1_Tgt.nc is built<br>
> The previous bash script relies on link to the /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/GRID/CREG025.L75-NEMO420_mesh_mask.nc file that has been used to perform the interpolation<br>
> The mean transport in GLORYS12V1 is compared to the one from Obs data of Woodgate et al. over the same period (2000-2015)

### Few steps:
- extract the correct grid with Extract_Bering_grid.bash
- Applyt the changes with the notebook
