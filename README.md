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
uv add "mcp[cli]" httpx
```

To run MCP server:
```bash
uv run mcp-server-hello
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

**Note:** To apply the changes in your code, just save and reload the configuration in Windsurl IDE.

**Note:** `mcp_server_hello/__main__.py` is the entry point allow you to run the server with `uv run mcp-server-hello` without installing the package.

## References

- [Official Doc](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Servers](https://github.com/modelcontextprotocol/servers)