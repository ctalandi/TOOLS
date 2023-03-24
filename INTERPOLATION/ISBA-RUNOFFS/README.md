## Scripts used to perform the remapping of ISBA data set on either CREG025.L75 or CREG12.L75 <br>
>
> The current scripts used are located on Jean-Zay (IDRIS) there /gpfswork/rech/cli/rost832/PRE-POST/ISBA-RUNOFFS/ <br>
> They have been shared by Jean-MArc Molines from IGE, look at there https://github.com/molines/IMHOTEP/blob/master/eORCA025/BUILD/RUNOFF_ISBA/README.md <br>
> The remapping relies python script build_CONFIG_runoff_interannual_fromISBA.py with CONFIG=CREG025.L75 or CREG12.L75<br> 
> The main script is launch.bash, just set the CONFIG <br>
> The final results is IA remapped ISBA runoffs <br> 
> To check the result and compare with Dai et al. data set, use the notebook ISBA-runoff_4CREG025.L75.ipynb on Datarmor located there /home1/datahome/ctalandi/DEV/FREDY/CONFIGS/CREG025.L75/ISBA-RUNOFF <br>

### One step:
- lanch the main script launch_job.bash
- control output fields on the CREG025.L75 grid using the notebook
