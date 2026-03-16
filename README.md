# Zotero MCP server

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-FastMCP-green.svg)](https://modelcontextprotocol.io)
[![Zotero API](https://img.shields.io/badge/Zotero-API%20v3-darkred.svg)](https://www.zotero.org/support/dev/web_api/v3/start)

A Model Context Protocol (MCP) server that connects AI assistants to your Zotero research library. Search papers, browse collections, and retrieve item details directly from your workflow.

## Setup

Install dependencies:
```bash
pip install mcp httpx python-dotenv
```

Create a `.env` file or export environment variables:
```bash
ZOTERO_API_KEY=your_api_key_here
ZOTERO_USER_ID=your_user_id_here
ZOTERO_LIBRARY_TYPE=user  # optional, defaults to "user"
```

Get your API key and User ID from https://www.zotero.org/settings/keys

## Usage

Run the server directly:
```bash
python zotero_mcp_server.py
```

Or add it to your Claude Code MCP config (`~/.claude/.mcp.json`):
```json
{
  "mcpServers": {
    "zotero": {
      "command": "python",
      "args": ["/path/to/zotero_mcp_server.py"],
      "cwd": "/path/to/zotero-mcp-server"
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `test_connection` | Test connectivity to the Zotero API |
| `search_items` | Search items by query string |
| `get_collections` | List all collections in the library |
| `get_item_details` | Get full metadata for a specific item |
| `get_recent_items` | Get recently added items |

## Resources

| URI | Description |
|-----|-------------|
| `zotero://collections` | All collections |
| `zotero://items` | All items (limit 50) |
| `zotero://recent` | Recently added items (limit 10) |
