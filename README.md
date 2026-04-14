# mcp-server-dummy

A dummy MCP server. Useless, but fancy.

## Setup

```bash
uv venv
source .venv/bin/activate
uv add "mcp[cli]" httpx click
```

## Run

```bash
# stdio (default)
uv run mcp-server-dummy

# SSE
uv run mcp-server-dummy --transport sse --port 8080

# Streamable HTTP
uv run mcp-server-dummy --transport streamable-http --port 8080
```

## Features

### Tools
| Tool | Description |
|---|---|
| `ping` | Responds with pong. Optionally echoes a message. |
| `echo` | Repeats back exactly what you send. |
| `lie` | Returns a confident, completely made-up fact. |
| `excuse` | Generates a professional excuse for any situation. |
| `vibe_check` | Scientifically measures a person's vibe score out of 100. |
| `motivate` | Delivers a hollow but enthusiastic motivational message. |

### Resources
| URI | Description |
|---|---|
| `dummy://status` | Current system status. Always reassuring. |
| `dummy://lorem` | Placeholder text, weird edition. |
| `dummy://advice` | Unsolicited life advice of dubious quality. |

### Prompts
| Prompt | Description |
|---|---|
| `nonsense` | Generate corporate-sounding gibberish about any topic. |
| `overengineer` | Explain something simple as a distributed systems nightmare. |

## Claude Code Integration

```bash
# STDIO
claude mcp add-json dummy '{"type":"stdio","command":"uv","args":["--directory","/path/to/mcp-server-dummy","run","mcp-server-dummy"]}'

# SSE
claude mcp add-json mcp-dummy-sse '{"type":"sse","url":"http://localhost:8080/sse"}'

# Streamable HTTP
claude mcp add-json mcp-dummy-http '{"type":"http","url":"http://localhost:8080/mcp"}'
```

## Windsurf IDE

Local:
```json
{
  "mcpServers": {
    "dummy": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/mcp-server-dummy", "run", "mcp-server-dummy"]
    }
  }
}
```

Remote:
```json
{
  "mcpServers": {
    "dummy": {
      "serverUrl": "http://localhost:8080/sse"
    }
  }
}
```

## References

- [MCP Docs](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
