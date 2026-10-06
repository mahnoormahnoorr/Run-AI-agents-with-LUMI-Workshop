## Add it to your harness

### OpenCode

On LUMI, the OpenCode container is already connected to the MCP server, so there is nothing to do. On your own machine, the `opencode.json` from the [previous chapter](/02_opencode#opencode-on-your-own-machine) already includes it.

### Claude Code

Run this once to make the server available in all your projects:

```bash
claude mcp add --transport http --scope user lumi-aif https://lumi-aif-agents.2.rahtiapp.fi/mcp
```

See the [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp) for other options.

### Codex

Add these lines to `~/.codex/config.toml`:

```toml title="~/.codex/config.toml"
[mcp_servers.lumi-aif]
url = "https://lumi-aif-agents.2.rahtiapp.fi/mcp"
```

See the [Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) for other options.

### Other harnesses

Most other harnesses and apps, such as VS Code, can connect to a remote MCP server too. Look in their documentation for how to add one, and give it the address `https://lumi-aif-agents.2.rahtiapp.fi/mcp`.

