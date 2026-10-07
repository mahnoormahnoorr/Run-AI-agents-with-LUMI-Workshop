# The sweep that hammered Slurm

About 30 minutes · CPU only · 20 short jobs, each under a minu

## The situation

A student needs to run the same small computation for 20 different settings. They wrote `submit_all.sh`, which "works on my laptop's Slurm test setup". On LUMI, a system administrator emailed them within the hour.

Do not run `submit_all.sh`. Your job is to find out why it is a problem, and replace it with something LUMI is happy with — using the agent to write it, and you to submit it.

What you're given
03-job-sweep/
├── make_configs.py   creates configs/config_00.json ... config_19.json
├── process.py        the computation for one config -- correct, don't change it
└── submit_all.sh     the student's submission script -- DO NOT RUN

`process.py` estimates π by random sampling for one config and writes a small JSON file to `results/`. It uses only the Python standard library.

## Background

Slurm's controller is shared by every user on LUMI. Each sbatch and squeue is a request to it, and a script that sends them in a tight loop slows the scheduler down for everyone. Submitting many tiny jobs one by one is also wasteful: Slurm has job arrays for running the same script over many inputs, with a built-in way to limit how many run at once.

## What to do

1. Create the configs yourself: `python3 make_configs.py` (light work, fine on a login node).
2. Start OpenCode in `03-job-sweep/` and ask the agent to review `submit_all.sh`: what does it do, and why would it cause trouble on a shared system? It should not run it — reject the request if it tries.
3. Ask it to write `sweep.sh`: a single Slurm job array over the 20 configs, CPU partition, one core, a short time limit, at most 5 running at once, with each task's output in its own log file. Ask it to check the LUMI documentation for the partition and limits.
4. Ask it to write `collect.py`, which reads `results/*.json` and prints the mean estimate of π and how many results it found.
5. Review both files, then submit from your second terminal and watch with `squeue --me `— a few times, by hand.
6. When the array has finished, run `python3 collect.py`.

## Done when

`collect.py` reports 20 results and a π estimate close to 3.14, all from one `sbatch` command, and `submit_all.sh` was never run.

## Going further
- Ask the agent how you could have known when the array finished without polling `squeue`. Check its answer in the documentation.
- Make one config fail on purpose (e.g. a negative `n`). How do you find which array task failed, and rerun only that one?
- Ask the agent to estimate how many scheduler requests the original script would have made. Do you agree with its reasoning?
