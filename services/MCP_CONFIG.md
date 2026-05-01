# FullStackArkham MCP Server Configuration

# For Claude Code (~/.claude/settings.json)
{
  "mcpServers": {
    "fullstackarkham": {
      "command": "python",
      "args": [
        "-m",
        "services.mcp_server"
      ],
      "cwd": "/Users/joeiton/Desktop/FullStackArkham",
      "env": {
        "DATABASE_URL": "postgresql://postgres:postgres@localhost:15432/fullstackarkham",
        "GATEWAY_URL": "http://localhost:8080",
        "MEDIA_COMMERCE_URL": "http://localhost:8087"
      }
    }
  }
}

# For Cursor (.cursor/settings.json)
{
  "mcp": {
    "servers": {
      "fullstackarkham": {
        "type": "stdio",
        "command": "python",
        "args": ["-m", "services.mcp_server"],
        "cwd": "/Users/joeiton/Desktop/FullStackArkham"
      }
    }
  }
}

# For Windsurf
# Add to windsurf.json in project root:
{
  "mcpServers": [
    {
      "name": "fullstackarkham",
      "command": "python",
      "args": ["-m", "services.mcp_server"],
      "cwd": "/Users/joeiton/Desktop/FullStackArkham"
    }
  ]
}
