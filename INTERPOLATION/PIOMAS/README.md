## Scripts used to perform the PIOMAS interpolation on CREG grids <br>
>
> The interpolation relies on the SCRIP package distributed with NEMO it has been done on Datarmor<br>
> 3 steps, #1 build the weights, #2 perform the interpolation, and #3 do a control  <br>
> The weights are built in the following directory: /home1/datawork/ctalandi/PRE-POST/FREDY/WEIGHTS with the wght.bash <br>
> - It relies on scripgrid.exe, scrip.exe and scripshape.exe available there /home1/datawork/ctalandi/WTOOLS/tools/WEIGHTS <br>
> input file are a tipycal PIOMAS field, such as heff1979.nc for instance and the domain_cfg file for either grid <br> 
> - From this step 2 fields area generated and usefull for the interpolation step: data_nemo_piomas_CREG025.L75_bilin_20230425.nc & reshape_PIOMAS_CREG025.L75_bilin_20230425.nc <br>
> only the reshape one is used for the online interpolation with NEMO, but here the 2 are required to perform an off-line interpolation <br> 
> 3 fields are concerned, area, snow and heff to setup an initial sea-ice state <br>
> It's done here: /home1/datawork/ctalandi/PRE-POST/FREDY/WEIGHTS/OFF-LINE/PIOMAS with the interp.bash script <br>
> It requires an input namelist called namelist_bilin_piomas_CREGXXX.tmp that will be changed by the interp.bash script and the 2 ones reshape_xxx and data_nemo_xxx<br> 
> - Then the final step is a control one to format a final file with a mask applied to fields and a gathering of 3 varaibles required heff, area and snow <br>
> The PIOMAS_clean.ipynb notebook does the job, with an output filename like CREGXX.L75_PIOMAS_yxxxx.nc <br>
> Finally a compresion is applied with ncks -4 -L A in.nc out.nc commmand line <br>
