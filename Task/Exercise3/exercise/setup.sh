#!/bin/bash
# One-time setup for the exercise. Run from inside the materials/ folder:
#     bash setup.sh project_46XXXXXXX
set -euo pipefail

# Path to the LUMI AI Factory PyTorch container (filled in by the organisers)
SIF_PATH="<path to the LUMI AI Factory PyTorch container>"

PROJECT="${1:-}"
if [[ ! "$PROJECT" =~ ^project_[0-9]+$ ]]; then
    echo "Usage: bash setup.sh project_46XXXXXXX   (your own LUMI project)" >&2
    exit 1
fi
cd "$(dirname "$0")"

# 1. Fill in the project and the container path in job.sh
sed -i "s|^#SBATCH --account=.*|#SBATCH --account=$PROJECT|" job.sh
sed -i "s|^SIF=.*|SIF=\"$SIF_PATH\"|" job.sh
echo "job.sh: account set to $PROJECT"
if [ ! -f "$SIF_PATH" ]; then
    echo "WARNING: container not found at $SIF_PATH" >&2
    echo "         Ask the organisers for the right path, and set SIF_PATH at the top of setup.sh." >&2
fi

# 2. Git: set up the repository and your identity, only if not done already
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git init -q
    echo "git: new repository created"
fi
git config user.name  >/dev/null || git config --global user.name  "$USER"
git config user.email >/dev/null || git config --global user.email "$USER@lumi"

# 3. Baseline commit (only if there is something new to commit)
git add .
if git diff --cached --quiet; then
    echo "git: nothing new to commit"
else
    git commit -q -m "baseline"
    echo "git: baseline committed"
fi

echo
echo "Ready. Next: sbatch job.sh   and   sbatch job.sh --profile"
