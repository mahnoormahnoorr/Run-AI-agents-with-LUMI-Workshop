# Run an AI agent on LUMI with OpenCode

In this part you start the OpenCode harness in the LUMI AI Factory container, connect it to an LLM on Aitta, and watch how an agent reads files, asks for permission and writes a job script for you to submit.

Time: about 40 minutes
You need: a LUMI account, your own LUMI project, and an Aitta API token [Aitta API Token](https://aitta-auth.csc.fi/myToken), choose your project)

> Before you start:
> every command the agent runs is executed under your user account, and you are responsible for it. Read the [LUMI AI agent guide](https://docs.lumi-supercomputer.eu/development/ai-tools/ai-agent-guide/), before your first session. Never give the agent sensitive or confidential data.

## 1. Prepare a safe working directory

Give the agent its own folder, under version control, so you can see and undo every change it makes.

```
ssh <username>@lumi.csc.fi

export PROJECT=project_46XXXXXXX          # your own LUMI project
mkdir -p /scratch/$PROJECT/$USER/ai-agent
cd /scratch/$PROJECT/$USER/ai-agent

git init
echo "print('hello from LUMI')" > hello.py
git add . && git commit -m "start"
```

## 2. Start OpenCode in the container

Run the harness in the ready-made LUMI container.

```
module load Local-LAIF lumi-aif-agents
opencode
```

## 3. Connect to Aitta and pick an LLM

Inside OpenCode:
1. Type `/connect` and search for aitta.
2. Paste your Aitta API token.
3. Pick an LLM from the list, or type `/models` and filter by `aitta`. Use the model your instructor names, for example Qwen3.6-27B.

Good to know:
- OpenCode saves the token in your home directory, so you only run `/connect` again when the token expires, after 90 days.
- Always check this line before your first prompt. It tells you where your prompts and files are sent.

## 4. Watch the agent loop

Ask: 

```
What's in this directory?
```

Choose Allow once.

> [!warning]
> Choose "Allow once" unless you are sure. "Allow always" lets the agent do that kind of action freely for the rest of the session, and the agent can also reach the folder where OpenCode keeps your API token.

## 5. Test the boundaries

Ask the agent each of these, one at a time. Read every permission request before answering.


```
Create hello.py.
Create a file notes.txt with today's date.
Delete hello.py.
Show me the files in my home directory.
List the files in /scratch/<your project>.
```
> Discuss: which of these would have been dangerous on your laptop without a container?

## 6. Give the agent one extra folder

Now, share data from outside the working directory, on purpose.
Exit OpenCode `(Ctrl+C)`, then:

```
mkdir -p /scratch/$PROJECT/$USER/extra-data
echo "sample data" > /scratch/$PROJECT/$USER/extra-data/readme.txt

export SINGULARITY_BIND=$SINGULARITY_BIND,/scratch/$PROJECT/$USER/extra-data
cd /scratch/$PROJECT/$USER/agent-lab
opencode
```

Ask: Read `/scratch/<your project>/<your user>/extra-data/readme.txt`.

The agent can now read the file. Folders you did not add stay invisible.

## 7. Let the agent write a job, submit it yourself

Use the agent for what it is good at, while you stay in charge of the shared system.

Ask:

```
Write a Slurm batch script job.sh for LUMI that runs hello.py on one CPU core
for 5 minutes, using account <your project>. Check the LUMI documentation for
the right partition. Do not try to submit it.
```

Approve the file write with Allow once. Then check the script yourself against [the LUMI Slurm documentation](https://docs.lumi-supercomputer.eu/runjobs/scheduled-jobs/batch-job/): account, partition, time limit and resources.

Submit it from a second terminal, outside the container:

```
cd /scratch/$PROJECT/$USER/ai-agent
sbatch job.sh
squeue --me
cat slurm-*.out        # after the job finishes
```

The output file contains `hello from LUMI`.

If it fails: paste the `sbatch` error into OpenCode and ask the agent to fix the script. Inside the container, `sbatch: command not found` is expected.

## 8. Review and save the agent's work

Ask:
```
Which git commands should I run to review and commit your changes?
```
Run the commands yourself, in your second terminal.


Optional: OpenCode on your own machine
On macOS or Linux:

curl -fsSL https://opencode.ai/install | bash


























