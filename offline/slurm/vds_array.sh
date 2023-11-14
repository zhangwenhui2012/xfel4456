#!/bin/bash

#SBATCH --array=1
#SBATCH --time=04:00:00
#SBATCH --partition=upex
##SBATCH --reservation=upex_004456
#SBATCH --export=ALL
#SBATCH -J vds
#SBATCH -o .%j.out
#SBATCH -e .%j.out

# Change the runs to process using the --array option on line 3

PREFIX=/gpfs/exfel/exp/SPB/202302/p004456

source /etc/profile.d/modules.sh
# Load modules and environment
module load exfel exfel-python

run=`printf %.4d "${SLURM_ARRAY_TASK_ID}"`
extra-data-make-virtual-cxi ${PREFIX}/raw/r${run} -o ${PREFIX}/scratch/vds/r${run}.cxi
