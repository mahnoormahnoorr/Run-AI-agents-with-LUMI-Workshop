# AI Agents on LUMI — Exercises

Three exercises to test what a coding agent can and cannot do for you on LUMI. You work with OpenCode in the LUMI AI Factory container, using an LLM on Aitta and the LUMI MCP server for documentation (see the hands-on guides Part 1 and Part 2).

All exercises are small: at most one GPU, and jobs run for seconds or minutes, not hours.

## Ground rules
1. You are in charge. Every command the agent runs is executed as you. Read every permission request; choose Allow once unless you are sure.
2. The agent writes, you submit. Slurm is not available inside the container. When a job script is ready, check it and run sbatch yourself from a second terminal.
3. Verify, don't trust. Ask the agent for links to the LUMI documentation it used, and open them.
4. Synthetic data only. Never give the agent sensitive data or credentials.

## The exercises

Each exercise has its own instructions file. Exercise 1 is a warm-up with no code: just follow its instructions. The other exercises come with code, in the directories listed below.

| # | Instructions | Code directory | Problem |
|---|---|---|---|
| 1 | [`exercise1`](https://github.com/mahnoormahnoorr/Run-AI-agents-with-LUMI-Workshop/blob/main/Task/Exercise1.md) | — | Find out what the agent can see, do and get wrong on LUMI. |
| 2 | [`exercise2`](https://github.com/mahnoormahnoorr/Run-AI-agents-with-LUMI-Workshop/tree/main/Task/Exercise2) | `laptop-to-lumi/` | A training script written for a laptop with an NVIDIA GPU has to run on LUMI. |
| 3 | [`exercise3`](exercise-03-job-sweep.md) | `03-job-sweep/` | A parameter sweep submits 20 jobs one by one and floods the Slurm scheduler. |


## Get started

Copy the exercise material from the shared project folder into your own scratch space, then start the agent there:

```bash
export PROJECT=project_462001520                          # your own LUMI project
mkdir -p /scratch/$PROJECT/$USER
cp -r /project/<workshop-project>/agent-workshop /scratch/$PROJECT/$USER/
cd /scratch/$PROJECT/$USER/agent-workshop

module load Local-LAIF lumi-aif-agents
opencode
```

In OpenCode, type `/connect`, search for **aitta** and paste your Aitta token, then pick the workshop model with `/models`. Check the status line shows the Aitta model **before** your first prompt.

We copy to `/scratch` rather than your home directory because the exercises create files and job output, and your home directory has a small quota. Remember that nothing on LUMI is backed up.

## Bring your own code

Once you have finished the warm-up exercise, you are welcome to work on your own code instead of the remaining exercises, for example your own research or a project you are curious about. 

## When something fails

Note it down. "The agent got this wrong" is a result, not a failure: one goal today is to learn where agents help and where they don't. Bring your examples to the wrap-up discussion

## Optional: share your session

If you are happy to help us improve the setup, export a session from your working directory:

```bash
opencode export > ~/agent-workshop-session.json
```

Select your session when asked, and send the file to the organisers. Check it first: it contains everything you typed and everything the agent read.
