## Scripts used to perform the ERA5 forcing interpolation on the CREG025.L75 grid <br>
>
> Job_interp_era5.pbs: <br>
> The current scripts used are located there /home1/datawork/ctalandi/PRE-POST/FREDY/WEIGHTS/OFF-LINE/ERA5 <br>
> It has been used to interpolate both scalars & vectors relying on the weights files data_nemo_era5_CREG025.L75_bicub_20220623.nc & data_nemo_era5_CREG025.L75_bilin_20220623.nc located there /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/RUNS/CREG025.L75/CREG025.L75-F/ in phase with the last CREG025.L75 version <br>
>
> wght_skt.bash and namelist_bilin_era5_skt: <br>
> Used to compute the weights for the ERA5 temperature correction skt <br>
> It has been done there: /home1/datawork/ctalandi/PRE-POST/FREDY/WEIGHTS/CREG025.L75 <br>
> Input files were: corrected_skt_2000_era5.nc & CREG025.L75_domain_cfg.nc (as coordinates.nc)  <br>
