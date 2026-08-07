"""
MCP (Model Context Protocol) integration for Wise Agent Toolkit.

This module provides integration with the Model Context Protocol standard,
allowing Wise Agent Toolkit to be used as an MCP server.
"""

# Check for MCP availability
try:
    from .server import serve, main
    from .toolkit import WiseAgentToolkit
    _MCP_AVAILABLE = True
except ImportError as e:
    _MCP_AVAILABLE = False
    _MCP_ERROR = str(e)

    # Provide fallback callables/classes
    def serve(*args, **kwargs):
        raise ImportError(
            "MCP is required for this functionality. "
            "Install it with: pip install wise-agent-toolkit[mcp]"
        )

    def main(*args, **kwargs):
        raise ImportError(
            "MCP is required for this functionality. "
            "Install it with: pip install wise-agent-toolkit[mcp]"
        )

    class WiseAgentToolkit:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "MCP is required for this functionality. "
                "Install it with: pip install wise-agent-toolkit[mcp]"
            )

__all__ = ["serve", "main", "WiseAgentToolkit", "_MCP_AVAILABLE"]
