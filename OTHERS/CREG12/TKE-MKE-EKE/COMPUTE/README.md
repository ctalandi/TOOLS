## Scripts used to perform the calculation of TKE, MKE and EKE for a CREG12.L75 experiment

All the following shell scripts, F90 code have been used on the ROME architecture
/ccc/work/cont003/gen7420/talandel/PRE-POST/SIM-OUTPUTS/DIAGS/ENERGETICS/CREG12.L75

  - cdfene.f90 relies on the original code cdfeke.f90, it has been adapeted to compute the TKE, MKE and EKE depending the arguments
  - launch_YearMean.bash & do_YearMean.bash.tmp > yearly mean of U & V fields using monthly means 
  - launch_mkeYE.bash & do_mkeYE.bash.tmp > yearly MKE using yearly mean U & V 
  - launch_tkeMO.bash & do_tkeMO.bash.tmp  > 5d mean EKE calculation and then monthly mean EKE. Anomalies are computed using annual mean of the considered year

  In the STORE-SAVE directory, scripts used to save results of the process above
  ' 
     .
     ├── cdfene.f90 
     ├── do_mkeYE.bash.tmp 
     ├── do_tkeMO.bash.tmp 
     ├── do_YearMean.bash.tmp 
     ├── launch_mkeYE.bash 
     ├── launch_tkeMO.bash 
     ├── launch_YearMean.bash 
     └── STORE-SAVE 
          ├── do_TarMKE-YE.bash.tmp 
          ├── do_TarTEKE.bash.tmp 
          ├── launch_TarMKE-YE.bash 
          └── launch_TarTEKE.bash 
  ' 

---
## CREG12.L75-REF08 dat location on the TGCC Store area

As a reminder the location of all REF08 data experiemnts: 

The monthly and annual means have been archived there:
/ccc/store/cont003/gen7420/talandel/CONFIGS/CREG12.L75/PACK-ARCHIVE/CREG12.L75-REF08-MEAN

To locate a specific year apply the following command: > grep y2005 *.toc

then to unpack the data go iinto the /ccc/work/cont003/gen7420/talandel/PRE-POST/UNPACK 
add the list of archive to be unpack in the launch_unpack.bash and launch it.
The tarfiles will be extracted and stored on the SCRATCH /ccc/scratch/cont003/gen7420/talandel/CREG12.L75/CREG12.L75-REF08-MEAN/5d

Then the last step required to detar the appropriate tar files by hand using screen env.


The 5d mean ooriginal outputs are located there: /ccc/store/cont003/gen7420/talandel/CONFIGS/CREG12.L75/CREG12.L75-REF08-S/5d/
control the availability of tarfiles using the command > ccc_hsm status * 

and use screen env. to get them locacly ccc_hsm get file

Once done the tarfiles can be copied on the SCRATCH /ccc/scratch/cont003/gen7420/talandel/CREG12.L75/CREG12.L75-REF08-S/5d

Then detar all files required
