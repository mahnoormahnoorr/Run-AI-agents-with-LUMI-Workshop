# Run an AI agent on LUMI with OpenCode

In this part you start the OpenCode harness in the LUMI AI Factory container, connect it to an LLM on Aitta, and watch how an agent reads files, asks for permission and writes a job script for you to submit.

Time: about 40 minutes
You need: a LUMI account, your own LUMI project, and an [Aitta API Token](https://aitta-auth.csc.fi/myToken), choose your project)

> Before you start:
> every command the agent runs is executed under your user account, and you are responsible for it. Read the [LUMI AI agent guide](https://docs.lumi-supercomputer.eu/development/ai-tools/ai-agent-guide/), before your first session. Never give the agent sensitive or confidential data.

## 1. Prepare a safe working directory

Give the agent its own folder, under version control, so you can see and undo every change it makes.

```
ssh <username>@lumi.csc.fi

export PROJECT=project_462001520          # your own LUMI project
mkdir -p /scratch/$PROJECT/$USER/ai-agent
cd /scratch/$PROJECT/$USER/ai-agent
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
opencode /scratch/$PROJECT/$USER/agent-lab
```

Ask: Read `/scratch/<your project>/<your user>/extra-data/readme.txt`.

The agent can now read the file. Folders you did not add stay invisible.

## 7. Let the agent write a job, submit it yourself

Use the agent for what it is good at, while you stay in charge of the shared system.

Ask:

```
First, create a Python script hello.py that prints "hello from LUMI", the hostname of the node it runs on, and the current date and time.

Then write a Slurm batch script job.sh for LUMI that runs hello.py on one CPU core for at most 5 minutes, using account <your project>. Check the LUMI documentation for the right partition, and write the job's output to a file named after the job ID.

Save both files in the current directory. Do not try to submit the job.
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


Optional: 

## OpenCode on your own machine

On macOS or Linux, the quickest way to install OpenCode is the official install script:

```bash
curl -fsSL https://opencode.ai/install | bash
```

For Windows and other options, such as npm, Homebrew and Docker, see the [OpenCode installation guide](https://opencode.ai/docs/).

Out of the box, OpenCode uses OpenCode Zen, a model service run by the company that maintains OpenCode, so everything you type and every file the agent reads is sent to that company. To add Aitta and the LUMI MCP server instead, download this configuration and save it as `~/.config/opencode/opencode.json`, or open the section below to copy it:

[opencode.json](./assets/opencode.json)

<details>
<summary>Show the contents of opencode.json</summary>

```json title="~/.config/opencode/opencode.json"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "aitta/Qwen/Qwen3.6-27B",
  "permission": {
    "bash": "ask",
    "edit": "ask",
    "webfetch": "ask",
    "websearch": "ask"
  },
  "mcp": {
    "lumi-aif": {
      "type": "remote",
      "url": "https://lumi-aif-agents.2.rahtiapp.fi/mcp",
      "enabled": true
    }
  },
  "provider": {
    "aitta": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Aitta",
      "options": {
        "baseURL": "https://aitta-api.csc.fi/openai/v1"
      },
      "models": {
        "openai/gpt-oss-120b": { "name": "openai/gpt-oss-120b" },
        "Qwen/Qwen3-Coder-Next": { "name": "Qwen/Qwen3-Coder-Next" },
        "Qwen/Qwen3.6-35B-A3B": { "name": "Qwen/Qwen3.6-35B-A3B" },
        "Qwen/Qwen3.6-27B": { "name": "Qwen/Qwen3.6-27B" },
        "Qwen/Qwen3-VL-30B-A3B-Thinking": { "name": "Qwen/Qwen3-VL-30B-A3B-Thinking" },
        "MiniMaxAI/MiniMax-M2.7": { "name": "MiniMaxAI/MiniMax-M2.7" },
        "google/gemma-4-31b-it": { "name": "google/gemma-4-31b-it" },
        "google/gemma-4-26B-A4B-it": { "name": "google/gemma-4-26B-A4B-it" },
        "mistralai/Ministral-3-14B-Reasoning-2512": { "name": "mistralai/Ministral-3-14B-Reasoning-2512" },
        "meta-llama/Llama-3.3-70B-Instruct": { "name": "meta-llama/Llama-3.3-70B-Instruct" },
        "LumiOpen/Llama-Poro-2-70B-Instruct": { "name": "LumiOpen/Llama-Poro-2-70B-Instruct" },
        "swiss-ai/Apertus-70B-Instruct-2509": { "name": "swiss-ai/Apertus-70B-Instruct-2509" },
        "swiss-ai/Apertus-8B-Instruct-2509": { "name": "swiss-ai/Apertus-8B-Instruct-2509" }
      }
    }
  }
}
```

</details>


























