#!/bin/bash

#SBATCH --array=21
#SBATCH --time=04:00:00
#SBATCH --partition=upex
##SBATCH --reservation=upex_004456
#SBATCH --export=ALL
#SBATCH -J vds
#SBATCH -o .%j.out
#SBATCH -e .%j.out

# Change the runs to process using the --array option on line 3

PREFIX=/gpfs/exfel/exp/SPB/202302/p004456

# for testing
PREFIX_test=/gpfs/exfel/exp/XMPL/201750/p700000

source /etc/profile.d/modules.sh
source ${PREFIX}/usr/Shared/amorgan/xfel3004/source_this_at_euxfel

run=`printf %.4d "${SLURM_ARRAY_TASK_ID}"`
extra-data-make-virtual-cxi ${PREFIX_test}/proc/r${run} -o ${PREFIX}/scratch/vds/r${run}.cxi

