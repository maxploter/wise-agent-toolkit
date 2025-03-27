from __future__ import annotations

from typing import Any, Optional, Type
from pydantic import BaseModel

from langchain.tools import BaseTool

from ..api import WiseAPI


class WiseTool(BaseTool):
    """Tool for interacting with the Wise API."""

    wise_api: WiseAPI
    method: str
    name: str = ""
    description: str = ""
    args_schema: Optional[Type[BaseModel]] = None

    def _run(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        """Use the Wise API to run an operation."""
        return self.wise_api.run(self.method, *args, **kwargs)