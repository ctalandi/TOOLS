# CREG12.L75-REF09 <br>
The way the domain_cfg file has been built for this experiment is detailed below<br>

## OVERVIEW
* Working directory on Rome: /ccc/workflash/cont003/gen7420/talandel/PRE-POST/DOMAIN-CFG
* Binaries used make_domain_cfg.exe & dom_doc.exe have benn compiled from there: /ccc/cont003/home/gen7420/talandel/DEV/DCM/DCM_4.2/DCMTOOLS/NEMOREF/NEMO4_r4.2.0/tools/DOMAINcfg/
   ** The first one is dedicated to the merge of 2 files, including a bathymetry and a coordinates file 
   ** The second one is used to insert in the domain_cfg file built previously all information coming from the namelist effectively used to built it (see the variable namelist_cfg) 
* Input files are listed below and are loacted there: /ccc/store/cont003/gen7420/talandel/CONFIGS/BUILD-CREG/CREG12.L75/CREG12.L75-I
   ** coordinates_CREG12_lbclnk_noz_vh20160930.nc
   ** bathymetry_CREG12_V3.3_REF09.nc 
* The job used is called launch_DomaCFG.pbs and is launched like ccc_msub launch_DomaCFG.pbs

