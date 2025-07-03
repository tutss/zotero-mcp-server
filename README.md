# Zotero MCP Server

A Model Context Protocol (MCP) server for interacting with Zotero research libraries.

## Setup

1. Install dependencies:
```bash
pip install mcp httpx python-dotenv
```

2. Set environment variables:
```bash
export ZOTERO_API_KEY=your_api_key_here
export ZOTERO_USER_ID=your_user_id_here
export ZOTERO_LIBRARY_TYPE=user  # optional, defaults to "user"
```

Get your API key and User ID from https://www.zotero.org/settings/keys

## Usage

Test connection:
```bash
python zotero_server_test.py
```

Run server:
```bash
python zotero_mcp_server.py
```

## Features

- **Resources**: Collections, items, recent items
- **Tools**: Search items, get collections, get item details, test connection
- **Authentication**: Secure API key-based authentication
- **Error handling**: Comprehensive error checking and logging

## MCP Integration

Compatible with MCP 1.10.1 and can be integrated with Claude Desktop or other MCP clients.