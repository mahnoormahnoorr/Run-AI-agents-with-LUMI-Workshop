# From laptop to LUMI

About 30 minutes · 1 GPU · the job runs for about a minute

## The situation

A colleague has a small PyTorch training script that runs fine on their laptop with an NVIDIA GPU. Their setup notes say: create a conda environment, `pip install torch`, check the GPU with `nvidia-smi`, run the script.

They want it running on LUMI by this afternoon. LUMI has AMD GPUs, no conda base environment, and a strong preference against installing Python packages yourself.

Your job: get it running on one LUMI GPU, using the agent and the LUMI documentation, without changing the model code.

## What you're given

02-laptop-to-lumi/

├── README_laptop.md   the colleague's setup notes -- written for a laptop

├── requirements.txt   what they pip-install

└── train_small.py     the training script -- correct, you should not need to change it

`train_small.py` trains a small network on random synthetic data, so it needs no dataset and no internet. It prints which device it found, the PyTorch version, the loss every 50 steps and the time per step.

## Background

On LUMI, PyTorch runs on AMD GPUs through ROCm. The PyTorch API still calls them `cuda` devices, which surprises people: code that uses `.cuda()` or `torch.device("cuda")` usually works unchanged. What does not carry over is the installation: a `pip install torch` gives you a build for NVIDIA GPUs, and Python environments with thousands of small files are hard on LUMI's shared file system. The LUMI AI Factory provides ready-made containers for this.

## What to do
1. Start OpenCode in `02-laptop-to-lumi/` and ask the agent to read `README_laptop.md` and explain what would not work on LUMI, with documentation links.
2. Ask it to write `job.sh`: a Slurm batch script that runs `train_small.py` on one GPU for at most 10 minutes, using a LUMI AI Factory container and your project account. Tell it not to install anything.
3. Check the script against the documentation pages it cites. Fix anything that doesn't match.
4. Submit it yourself from your second terminal, and read the output.
5. If the job fails, paste the error into OpenCode and iterate.

## Done when
The output file shows an AMD Instinct device name, the loss going down, and a time per step, and `git diff` shows that `train_small.py` was not changed.
One warning, because it costs people time: if the agent's first idea is a `pip install`, a `conda create` or a virtual environment, push back and ask it to check the LUMI documentation for containers first.

## Going further
Ask the agent: 
- Run with `--steps 2000` and compare the time per step with a CPU-only run (`--cpu`). Is the GPU worth it at this size? At `--hidden 4096`?
- Ask the agent to write an updated `README_lumi.md` for the colleague. Would you send it as is?
- Ask what the job was charged for. Does requesting more memory or CPU cores change the billing on a GPU partition?
