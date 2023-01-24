## Scripts used to drown over land values of ERA5 dataset <br>
>
> launch_drown.bash: <br>
> The master script that loop over years and each variable to be drowned<br>
>
> Sosie_ERA5_drown.slurm.tmp: <br>
> The job (Datarmor header) that relies on Sosie binary mask_drown_field.x<br>
> Need 2 inputs fields, the variable file with an unlimited time axis & the ERA5 land sea mask <br>
> 1 job / variable and year is submitted to speed-up the process <br>
>
