The LUMI AI Factory runs a public MCP server that fills this gap. It lets your agent look things up in the LUMI documentation and check LUMI's current status, so it can answer questions about LUMI more accurately and write code suited to the system. It works with any harness or app that supports MCP, such as OpenCode, Claude Code, Codex or VS Code, whichever LLM it uses. You do not need an account or an API token to use it.

## What it can do

The LUMI MCP server gives your agent two tools:

| Tool | What it does | Helps with questions like |
|:-----|:-------------|:--------------------------|
| `retrieve_docs` | Searches a regularly updated knowledge base of the [LUMI documentation](https://docs.lumi-supercomputer.eu/) and the [LUMI AI Guide](https://github.com/Lumi-supercomputer/LUMI-AI-Guide), and returns the most relevant passages with links to their sources | "How do I run PyTorch on LUMI?" |
| `get_service_status` | Reports LUMI's current status, planned maintenance and ongoing incidents | "Why is my job not starting? Is something down?" |


## 1. Find the MCP tools in OpenCode

On LUMI, the OpenCode container is already connected to the MCP server, so there is nothing to set up.

```bash
export PROJECT=project_46XXXXXXX
cd /scratch/$PROJECT/$USER/agent-lab
module load Local-LAIF lumi-aif-agents
opencode
```

Check that an Aitta LLM is selected ([see here](https://github.com/mahnoormahnoorr/Run-AI-agents-with-LUMI-Workshop/tree/main/Hands-on/OpenCode#3-connect-to-aitta-and-pick-an-llm)), then ask:  

```bash
Which tools do you have from the LUMI MCP server, and what does each one do?
How's LUMI doing right now?
```
## 2. See exactly what the agent receives

call retrieve_docs yourself, without any agent or LLM involved.
Run this in a terminal on LUMI or on your laptop. No login or token is needed:

```bash
module load cray-python/3.11.7
pip install fastmcp
fastmcp list https://lumi-aif-agents.2.rahtiapp.fi/mcp
fastmcp call https://lumi-aif-agents.2.rahtiapp.fi/mcp \
    retrieve_docs 'query=how to use pytorch on lumi' 'k=2'
```



