# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server implementation that provides greeting tools and joke resources. The server can run in two transport modes: stdio (default) for direct MCP client integration, and SSE (Server-Sent Events) over HTTP for web-based integrations.

## Common Commands

**Install/sync dependencies:**
```bash
uv sync
```

**Run the MCP server:**
```bash
uv run mcp-server-hello
```

**Run with SSE transport on custom port:**
```bash
uv run mcp-server-hello --transport sse --port 8080
```

**Format code:**
```bash
black mcp_server_hello/
```

## Architecture

### Core Components

- **mcp_server_hello/server.py**: Main server implementation using the low-level MCP Server API
  - Tools: hello, bye, compliment, roast (all require a "name" parameter)
  - Resources: jokes://random (single joke) and jokes://all (all jokes as JSON)
  - Transport support: stdio and SSE via Starlette/uvicorn

- **mcp_server_hello/__main__.py**: Entry point that enables `uv run mcp-server-hello`

### Transport Architecture

The server supports two transport modes:
- **stdio**: Direct MCP protocol communication for local clients
- **SSE**: HTTP-based transport using Starlette web framework with SSE endpoints at `/sse` and `/messages/`

### Tool Pattern

All tools follow the same pattern:
1. Validate required "name" parameter exists
2. Call corresponding function (say_hello, say_bye, give_compliment, give_roast)
3. Return single text ContentBlock

### Resource Pattern

Resources use custom URI scheme "jokes://" with two endpoints:
- `jokes://random`: Returns random joke as text/plain
- `jokes://all`: Returns all jokes as application/json

## IDE Integration

**Windsurl IDE local config:**
```json
{
  "mcpServers": {
    "hello": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/mcp-server-hello", "run", "mcp-server-hello"]
    }
  }
}
```

**Windsurl IDE remote config (SSE):**
```json
{
  "mcpServers": {
    "hello": {
      "serverUrl": "http://localhost:8000/sse"
    }
  }
}
```