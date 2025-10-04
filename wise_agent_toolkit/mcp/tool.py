"""
MCP Tool implementation for Wise Agent Toolkit.

Provides MCP-compatible tool wrapper for Wise API operations.
"""

import json
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel

from ..integrations.base import BaseIntegrationTool
from ..api import WiseAPI

# Check for MCP availability
try:
    from mcp.types import Tool, TextContent
    _MCP_AVAILABLE = True
except ImportError:
    _MCP_AVAILABLE = False
    # Provide fallback types
    class Tool:
        def __init__(self, *args, **kwargs):
            pass

    class TextContent:
        def __init__(self, *args, **kwargs):
            pass


class WiseTool(BaseIntegrationTool):
    """MCP-compatible tool for Wise API operations."""

    def __init__(
        self,
        name: str,
        description: str,
        method: str,
        wise_api: WiseAPI,
        args_schema: Optional[Type[BaseModel]] = None,
    ):
        if not _MCP_AVAILABLE:
            raise ImportError(
                "MCP is required for this functionality. "
                "Install it with: pip install wise-agent-toolkit[mcp]"
            )

        super().__init__(
            wise_api=wise_api,
            method=method,
            name=name,
            description=description,
            args_schema=args_schema
        )

    def to_mcp_tool(self) -> Tool:
        """Convert to MCP Tool format."""
        input_schema = {}
        if self.args_schema:
            input_schema = self.args_schema.model_json_schema()

        return Tool(
            name=self.name,
            description=self.description,
            inputSchema=input_schema
        )

    def execute(self, arguments: Dict[str, Any]) -> str:
        """Execute the tool with MCP-formatted arguments."""
        try:
            # Use the WiseAPI.run method to execute the tool
            result = self.wise_api.run(self.method, **arguments)
            return result

        except Exception as e:
            return f"Error executing {self.method}: {str(e)}"

    async def call(self, arguments: Dict[str, Any]) -> list[TextContent]:
        """MCP-compatible call method."""
        result = self.execute(arguments)
        return [TextContent(
            type="text",
            text=result
        )]