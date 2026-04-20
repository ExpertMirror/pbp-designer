#!/bin/bash
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --time=0-03:00:00
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --account=rrg-dwishart

export HF_HOME=$SCRATCH/huggingface
export HF_HUB_CACHE=$SCRATCH/huggingface/hub
export TRANSFORMERS_CACHE=$SCRATCH/huggingface/transformers

module load apptainer
module load python/3.14.2
module load rdkit

unset SSL_CERT_FILE
unset REQUESTS_CA_BUNDLE
unset CURL_CA_BUNDLE

python run.py "C1C[C@H](NC1)C(=O)O" proline1
