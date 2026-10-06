The LUMI AI Factory runs a public MCP server that fills this gap. It lets your agent look things up in the LUMI documentation and check LUMI's current status, so it can answer questions about LUMI more accurately and write code suited to the system. It works with any harness or app that supports MCP, such as OpenCode, Claude Code, Codex or VS Code, whichever LLM it uses. You do not need an account or an API token to use it.

## What it can do

The LUMI MCP server gives your agent two tools:

| Tool | What it does | Helps with questions like |
|:-----|:-------------|:--------------------------|
| `retrieve_docs` | Searches a regularly updated knowledge base of the [LUMI documentation](https://docs.lumi-supercomputer.eu/) and the [LUMI AI Guide](https://github.com/Lumi-supercomputer/LUMI-AI-Guide), and returns the most relevant passages with links to their sources | "How do I run PyTorch on LUMI?" |
| `get_service_status` | Reports LUMI's current status, planned maintenance and ongoing incidents | "Why is my job not starting? Is something down?" |


## 
