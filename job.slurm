#!/bin/bash -l
#
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --export=NONE

unset SLURM_EXPORT_ENV

module add python
conda activate YOUR_ENVIRONMENT

python3 mainPipeline.py --workdir "$WORK"