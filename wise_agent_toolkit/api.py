from __future__ import annotations

import json
from typing import Optional

import wise_api_client
from pydantic import BaseModel
from wise_api_client import ApiClient

from .configuration import Context
from .functions import (
    create_transfer, create_quote,
)


class WiseAPI(BaseModel):
    """Wrapper for Wise API"""

    _context: Context
    _api_client: ApiClient

    def __init__(self, api_key: str, host: str, context: Optional[Context]):
        super().__init__()

        self._context = context if context is not None else Context()

        configuration = wise_api_client.Configuration(
            access_token=api_key,
            host=host,
        )
        self._api_client = wise_api_client.ApiClient(configuration)

    def run(self, method: str, *args, **kwargs) -> str:
        if method == "create_transfer":
            transfer = create_transfer(self._api_client, self._context, *args, **kwargs).to_dict()
            return json.dumps(
                transfer,
                default=str # to_dict() does not serialize datetime objects
            )
        elif method == "create_quote":
            quote = create_quote(self._api_client, self._context, *args, **kwargs).to_dict()
            return json.dumps(
                quote,
                default=str # to_dict() does not serialize datetime objects
            )
        elif method == "create_recipient":
            raise NotImplementedError("create_recipient method is not implemented.")
        elif method == "list_recipients":
            raise NotImplementedError("list_recipients method is not implemented.")
        else:
            raise ValueError("Invalid method " + method)
