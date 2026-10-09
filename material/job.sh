#!/bin/bash
#SBATCH --job-name=slow-training
#SBATCH --account=project_46XXXXXXX
#SBATCH --partition=small-g
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=7
#SBATCH --mem=60G
#SBATCH --time=00:15:00
#SBATCH --output=%x_%j.out

# Load the LUMI AI Factory bind-mount setup (sets SINGULARITY_BIND)
module use /appl/local/laifs/modules
module load lumi-aif-singularity-bindings

# LUMI AI Factory PyTorch container (path from the LUMI AI Factory documentation)
SIF="<path to the LUMI AI Factory PyTorch container>"

if [ ! -f "$SIF" ]; then
    echo "ERROR: container not found: $SIF" >&2
    echo "Run 'bash setup.sh <your project>' first, or ask the organisers for the container path." >&2
    exit 1
fi

# Arguments given to sbatch after job.sh (e.g. --profile) are passed on to the script
srun singularity exec "$SIF" python3 train_shapes.py "$@"
