# Run an AI agent on LUMI with OpenCode

In this part you start the OpenCode harness in the LUMI AI Factory container, connect it to an LLM on Aitta, and watch how an agent reads files, asks for permission and writes a job script for you to submit.

Time: about 40 minutes
You need: a LUMI account, your own LUMI project, and an Aitta API token [Aitta API Token](https://aitta-auth.csc.fi/myToken), choose your project)

> Before you start:
> every command the agent runs is executed under your user account, and you are responsible for it. Read the [LUMI AI agent guide](https://docs.lumi-supercomputer.eu/development/ai-tools/ai-agent-guide/), before your first session. Never give the agent sensitive or confidential data.

## Prepare a safe working directory

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

## Start OpenCode in the container

Run the harness in the ready-made LUMI container.

```
module load Local-LAIF lumi-aif-agents
opencode
```

#3 Connect to Aitta and pick an LLM

Inside OpenCode:
1. Type /connect and search for aitta.
2. Paste your Aitta API token.
3. Pick an LLM from the list, or type /models and filter by aitta. Use the model your instructor names, for example Qwen3.6-27B.

Good to know:
- OpenCode saves the token in your home directory, so you only run /connect again when the token expires, after 90 days.
- Always check this line before your first prompt. It tells you where your prompts and files are sent.

## Watch the agent loop

Ask: 

```
What's in this directory?
```

Choose Allow once.

> [!warning]
> Choose "Allow once" unless you are sure. "Allow always" lets the agent do that kind of action freely for the rest of the session, and the agent can also reach the folder where OpenCode keeps your API token.





