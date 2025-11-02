# mcp-server-hello

To setup:

```bash
# Create a new directory for our project
uv init <project_name>
cd <project_name>

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]" httpx click black
```

To run MCP server:
```bash
# stdio
uv run mcp-server-hello

# sse
uv run mcp-server-hello --transport sse --port 8080


# streamable-http
uv run mcp-server-hello --transport streamable-http --port 8080
```

Windsurl IDE local configuration:

```json
{
  "mcpServers": {
    "hello": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-server-hello",
        "run",
        "mcp-server-hello"
      ]
    }
  }
}
```
Windsurl IDE remote configuration:

```json
{
  "mcpServers": {
    "hello": {
      "serverUrl": "http://localhost:8000/sse"
    }
  }
}
```

Claude code integration:

```bash
# STDIO
claude mcp add-json hello '{"type":"stdio","command":"uv","args":["--directory","/home/locch/Works/mcp-server-hello","run","mcp-server-hello"]}'

# SSE
claude mcp add-json mcp-hello-sse '{"type":"sse","url":"http://localhost:8080/sse"}'
# Or with authentication
claude mcp add-json mcp-hello-sse '{"type":"sse","url":"http://localhost:8080/sse","headers":{"Authorization":"Bearer your-token","X-API-Key":"your-key"}}'

# STREAMALBE-HTTP
claude mcp add-json mcp-hello-sse '{"type":"sse","url":"http://localhost:8080/sse","headers":{"Authorization":"Bearer your-token","X-API-Key":"your-key"}}'
claude mcp add-json mcp-hello-http '{"type":"http","url":"http://localhost:8080/mcp","headers":{"Authorization":"Bearer your-token","Content-Type":"application/json"}}'
```


**Note:** To apply the changes in your code, just save and reload the configuration in Windsurl IDE.

**Note:** `mcp_server_hello/__main__.py` is the entry point allow you to run the server with `uv run mcp-server-hello` without installing the package.

## References

- [Official Doc](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Servers](https://github.com/modelcontextprotocol/servers)