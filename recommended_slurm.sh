#!/bin/bash
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=0-03:00:00
#SBATCH --account=example-account
#SBATCH --output=serine_run.out

module load apptainer # Apptainer is required to run BoltzGen, ColabFold, Autodock Vina, etc.

unset SSL_CERT_FILE #It is a good idea to unset your CERT path before attempting to send transacctions to the web. Otherwise, your SLURM job may fail.
unset REQUESTS_CA_BUNDLE
unset CURL_CA_BUNDLE

module load python/3.14.2 #PBP designer requires python 3.14.X
module load rdkit #Some of the required dependancies may already exist as a module on your HPC cluster. Try running the pipeline without loading any python packages, and the error messages will tell you what packages must be loaded to begin.

python run.py "C([C@@H](C(=O)O)N)O" thc_binder

#Required usage: python run.py <SMILES code in quotations> <project_name>
