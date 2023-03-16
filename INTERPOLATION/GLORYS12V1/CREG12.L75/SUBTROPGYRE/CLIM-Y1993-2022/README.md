## Scripts used to perform a climatology over 1993-2022 <br>
>
> The current scripts used are located there /home1/datawork/ctalandi/PRE-POST/FREDY/BUILD-BDYS/CREG12.L75/SUBTROPGYRE/CLIM-Y1993-2022 <br>
> The main script is launch_clim.bash, select either to compute leap years or the seasonal cycle <br>
> The final directories where are stored the data is /home/datawork-lops-drakkarcom/SIMULATION-OUTPUTS/FREDY/CONFIGS/CREG12.L75/BDYS/SUBTROPGYRE/ with NOLEAP and CLIM-Y1993-2022  <br> 

### Few steps:
- remove the 29th day for each leap year, 1996, 2000, 2004, 2008, 2012, 2016 and 2020
- compute the seasonal cycle 
- manage prperly the _FillValue 
