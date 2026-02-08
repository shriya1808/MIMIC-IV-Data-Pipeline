#!/bin/bash -l
#
#SBATCH --ntasks=1
#SBATCH --time=1:00:00
#SBATCH --export=NONE

unset SLURM_EXPORT_ENV

WORKDIR="$WORK/MIMIC-IV-Data-Pipeline"
cd "$WORKDIR" || exit 1
echo "Running in: $(pwd)"

source ~/.bashrc
export http_proxy=http://proxy.nhr.fau.de:80
export https_proxy=http://proxy.nhr.fau.de:80

if [ ! -f ~/.bash_profile ]; then
  echo "if [ -f ~/.bashrc ]; then . ~/.bashrc; fi" > ~/.bash_profile
fi

module add python
conda config --add pkgs_dirs $WORK/software/private/conda/pkgs
conda config --add envs_dirs $WORK/software/private/conda/envs
conda env create -f environment.yml -y
conda config --set channel_priority strict
conda activate mimic-pipeline
conda install -c conda-forge tqdm scikit-learn imbalanced-learn nltk -y
conda install -c conda-forge ipywidgets pytorch -y
pip install import-ipynb captum PyRuSH medspacy
pip install Jinja2==2.11.2
conda install ipykernel -y


python3 mainPipeline.py --workdir "$WORK/MIMIC-IV-Data-Pipeline/"