
qsub -I -l select=1:ncpus=1:mem=20gb -l walltime=10:00:00 -q ftp -S /bin/bash

