"""
MCP Server implementation for Wise Agent Toolkit.

Provides a complete MCP server that exposes Wise API operations as MCP tools.
"""

import logging
import argparse
import os
from typing import Optional
from pathlib import Path

# Handle imports for both module and standalone execution
try:
  from ..configuration import Configuration, Context, ACTIONS_ALL
  from ..api import WiseAPI
  from .toolkit import WiseAgentToolkit
except ImportError:
  # If relative imports fail, try absolute imports
  import sys

  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
  from wise_agent_toolkit.configuration import Configuration, Context
  from wise_agent_toolkit.api import WiseAPI
  from wise_agent_toolkit.mcp.toolkit import WiseAgentToolkit

# Check for MCP availability
try:
  from mcp.server import Server
  from mcp.server.stdio import stdio_server
  from mcp.types import TextContent, Tool, ListToolsResult, CallToolResult

  _MCP_AVAILABLE = True
except ImportError:
  _MCP_AVAILABLE = False
  Server = None


def build_server(toolkit: WiseAgentToolkit, server_name: str = "wise-agent-toolkit") -> "Server":
  """Build an mcp.server.Server wired up to the given toolkit's tools.

  Split out from serve() so tests (and any other embedder) can exercise the
  request handlers directly, without going through stdio.
  """
  logger = logging.getLogger(__name__)

  # Create a dictionary mapping tool names to tool instances
  tool_name_and_tool = {tool.name: tool for tool in toolkit.get_tools()}

  async def on_list_tools(ctx, params) -> ListToolsResult:
    """List all available Wise API tools."""
    tools: list[Tool] = [tool.to_mcp_tool() for tool in tool_name_and_tool.values()]
    return ListToolsResult(tools=tools)

  async def on_call_tool(ctx, params) -> CallToolResult:
    """Execute a Wise API tool."""
    name = params.name
    arguments = params.arguments or {}

    tool = tool_name_and_tool.get(name)
    if tool is None:
      return CallToolResult(
        content=[TextContent(type="text", text=f"Tool '{name}' not found")],
        is_error=True,
      )

    try:
      result = tool.execute(arguments)
      return CallToolResult(content=[TextContent(type="text", text=result)])
    except Exception as e:
      logger.error(f"Error executing tool {name}: {str(e)}")
      return CallToolResult(
        content=[TextContent(type="text", text=f"Error executing {name}: {str(e)}")],
        is_error=True,
      )

  return Server(server_name, on_list_tools=on_list_tools, on_call_tool=on_call_tool)


async def serve(
  api_key: str,
  host: str = "https://api.sandbox.transferwise.tech",
  server_name: str = "wise-agent-toolkit",
  profile_id: Optional[int] = None
) -> None:
  """Serve the MCP server."""
  logger = logging.getLogger(__name__)

  if not _MCP_AVAILABLE:
    logger.error("MCP is not available. Install it with: pip install wise-agent-toolkit[mcp]")
    return

  # Initialize the API client and toolkit locally
  context = Context(profile_id=profile_id)
  toolkit = WiseAgentToolkit(
    api_key=api_key,
    host=host,
    configuration={"actions": ACTIONS_ALL, "context": context}
  )

  server = build_server(toolkit, server_name=server_name)

  # Run the server
  options = server.create_initialization_options()
  async with stdio_server() as (read_stream, write_stream):
    await server.run(read_stream, write_stream, options, raise_exceptions=True)


def main():
  """Main entry point for running the MCP server."""
  # Set up logging to stderr
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # This writes to stderr by default
  )
  logger = logging.getLogger(__name__)

  parser = argparse.ArgumentParser(description="Wise Agent Toolkit MCP Server")
  parser.add_argument(
    "--api_key",
    default=os.getenv("WISE_API_KEY"),
    help="Wise API key (default: from WISE_API_KEY environment variable)"
  )
  parser.add_argument(
    "--host",
    default=os.getenv("WISE_API_HOST", "https://api.sandbox.transferwise.tech"),
    help="Wise API host (default: from WISE_API_HOST environment variable or sandbox)"
  )
  parser.add_argument(
    "--server_name",
    default="wise-agent-toolkit",
    help="MCP server name"
  )
  parser.add_argument(
    "--profile_id",
    type=int,
    default=None,
    help="Wise profile ID"
  )

  args = parser.parse_args()

  if not args.api_key:
    logger.error("API key is required. Provide it via --api-key or WISE_API_KEY environment variable.")
    return

  import asyncio
  asyncio.run(serve(
    api_key=args.api_key,
    host=args.host,
    server_name=args.server_name,
    profile_id=args.profile_id,
  ))


if __name__ == "__main__":
  main()
