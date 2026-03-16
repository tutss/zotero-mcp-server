#!/usr/bin/env python3

import json
import logging
import os
import sys
from urllib.parse import quote

from dotenv import load_dotenv
import httpx
from mcp.server.fastmcp import FastMCP

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("zotero-mcp-server")

API_KEY = os.getenv("ZOTERO_API_KEY", "")
USER_ID = os.getenv("ZOTERO_USER_ID", "")
LIBRARY_TYPE = os.getenv("ZOTERO_LIBRARY_TYPE", "user")
BASE_URL = f"https://api.zotero.org/{LIBRARY_TYPE}s/{USER_ID}"

mcp = FastMCP("zotero")


async def _zotero_request(endpoint: str) -> dict | list:
    headers = {
        "Zotero-API-Key": API_KEY,
        "Content-Type": "application/json",
    }
    url = f"{BASE_URL}/{endpoint}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 403:
            raise Exception("Authentication failed - check your API key and permissions")
        if response.status_code == 404:
            raise Exception("Resource not found - check your user ID and library type")
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def test_connection() -> str:
    """Test connection to Zotero API."""
    try:
        collections = await _zotero_request("collections?limit=1")
        return json.dumps({
            "status": "success",
            "message": "Successfully connected to Zotero API",
            "collections_found": len(collections),
        }, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}, indent=2)


@mcp.tool()
async def search_items(query: str, limit: int = 10) -> str:
    """Search items in Zotero library."""
    results = await _zotero_request(f"items?q={quote(query)}&limit={limit}")
    return json.dumps(results, indent=2)


@mcp.tool()
async def get_collections() -> str:
    """Get all collections in the Zotero library."""
    collections = await _zotero_request("collections")
    return json.dumps(collections, indent=2)


@mcp.tool()
async def get_item_details(item_key: str) -> str:
    """Get detailed information about a specific Zotero item."""
    item = await _zotero_request(f"items/{item_key}")
    return json.dumps(item, indent=2)


@mcp.tool()
async def get_recent_items(limit: int = 10) -> str:
    """Get recently added items from the Zotero library."""
    items = await _zotero_request(f"items?limit={limit}&sort=dateAdded&direction=desc")
    return json.dumps(items, indent=2)


@mcp.resource("zotero://collections")
async def collections_resource() -> str:
    """List all collections in your Zotero library."""
    collections = await _zotero_request("collections")
    return json.dumps(collections, indent=2)


@mcp.resource("zotero://items")
async def items_resource() -> str:
    """All items in your Zotero library."""
    items = await _zotero_request("items?limit=50")
    return json.dumps(items, indent=2)


@mcp.resource("zotero://recent")
async def recent_resource() -> str:
    """Recently added items."""
    items = await _zotero_request("items?limit=10&sort=dateAdded&direction=desc")
    return json.dumps(items, indent=2)


if __name__ == "__main__":
    if not API_KEY:
        sys.stderr.write("ZOTERO_API_KEY environment variable is missing\n")
        sys.exit(1)
    if not USER_ID:
        sys.stderr.write("ZOTERO_USER_ID environment variable is missing\n")
        sys.exit(1)
    mcp.run()
