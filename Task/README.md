# AI Agents on LUMI — Exercises

Three exercises to test what a coding agent can and cannot do for you on LUMI. You work with OpenCode in the LUMI AI Factory container, using an LLM on Aitta and the LUMI MCP server for documentation (see the hands-on guides Part 1 and Part 2).

All exercises are small: at most one GPU, and jobs run for seconds or minutes, not hours.

## Ground rules
1. You are in charge. Every command the agent runs is executed as you. Read every permission request; choose Allow once unless you are sure.
2. The agent writes, you submit. Slurm is not available inside the container. When a job script is ready, check it and run sbatch yourself from a second terminal.
3. Verify, don't trust. Ask the agent for links to the LUMI documentation it used, and open them.
4. Synthetic data only. Never give the agent sensitive data or credentials.

## When something fails

Note it down. "The agent got this wrong" is a result, not a failure: one goal today is to learn where agents help and where they don't. Bring your examples to the wrap-up discussion

## Optional: share your session

If you are happy to help us improve the setup, export a session from your working directory:

```bash
opencode export > ~/agent-workshop-session.json
```

Select your session when asked, and send the file to the organisers. Check it first: it contains everything you typed and everything the agent read.
