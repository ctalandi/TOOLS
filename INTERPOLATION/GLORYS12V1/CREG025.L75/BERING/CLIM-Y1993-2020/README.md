## Scripts used to perform a climatology over 1993-2020 <br>
>
> The current scripts used are located there /home1/datawork/ctalandi/PRE-POST/FREDY/BUILD-BDYS/CREG025.L75/BERING/CLIM-Y1993-2020 <br>
> The main script is launch_clim.bash, select 1st to compute leap years 1nd to build the seasonal cycle <br>
> The final directories where are stored the data is /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG025.L75/BDYS/BERING/ with NOLEAP and CLIM-Y1993-2020  <br> 

### Few steps:
- remove the 29th day for each leap year, 1996, 2000, 2004, 2008, 2012, 2016 and 2020
- compute the seasonal cycle 
- manage properly the _FillValue 
