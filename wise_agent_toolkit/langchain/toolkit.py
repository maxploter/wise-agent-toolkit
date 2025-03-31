from typing import List, Optional
from pydantic import PrivateAttr

from ..api import WiseAPI
from ..tools import tools
from ..configuration import Configuration, Context, is_tool_allowed
from .tool import WiseTool

class WiseAgentToolkit:
    _tools: List = PrivateAttr(default=[])

    def __init__(
        self,
        api_key: str,
        host: str = "https://api.sandbox.transferwise.tech",
        configuration: Optional[Configuration] = None
    ):
        super().__init__()

        context = configuration.get("context") if configuration else None

        wise_api = WiseAPI(api_key=api_key, host=host, context=context)

        filtered_tools = [
            tool for tool in tools if is_tool_allowed(tool, configuration)
        ]

        self._tools = [
            WiseTool(
                name=tool["method"],
                description=tool["description"],
                method=tool["method"],
                wise_api=wise_api,
                args_schema=tool.get("args_schema", None),
            )
            for tool in filtered_tools
        ]

    def get_tools(self) -> List:
        """Get the tools in the toolkit."""
        return self._tools
