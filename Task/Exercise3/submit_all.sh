#!/bin/bash
# !!! WORKSHOP EXERCISE -- DO NOT RUN THIS SCRIPT !!!
# It is here to be reviewed. Running it would flood the Slurm scheduler.
echo "This script is for review only. See exercise-03-job-sweep.md." && exit 1

# Runs all 20 configs. Worked on my laptop's test cluster.
for i in $(seq -w 0 19); do
    sbatch --account=project_XXXXXXXXX --partition=small --time=00:05:00 \
           --wrap="python3 process.py configs/config_$i.json"

    # wait until this job is done before submitting the next one
    while squeue -u $USER | grep -q wrap; do
        squeue -u $USER
    done
done
echo "all done"
