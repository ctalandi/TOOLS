#!/bin/bash

# Either CREG12 or CREG025
#CONF=CREG025 
CONF=CREG12 

sed -e "s/<XXCONFXX>/${CONF}/g" job_runoffs_IA.sbatch.tmp > job_runoffs_IA_${CONF}.sbatch

sbatch job_runoffs_IA_${CONF}.sbatch 
