from __future__ import annotations

import json
from typing import Optional

import wise_api_client
from pydantic import BaseModel
from wise_api_client import ApiClient

from .configuration import Context
from .functions import (
  create_transfer, create_quote, update_quote, list_recipient_accounts, create_recipient_account,
  deactivate_recipient_account, list_transfers, cancel_transfer, get_transfer_by_id, list_profiles,
  get_profile_by_id, get_quote_by_id, get_recipient_account_by_id,
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
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "create_quote":
      quote = create_quote(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(
        quote,
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "update_quote":
      quote = update_quote(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(
        quote,
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "list_recipient_accounts":
      recipients = list_recipient_accounts(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(recipients, default=str)  # to_dict() does not serialize datetime objects
    elif method == "create_recipient_account":
      recipient = create_recipient_account(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(
        recipient,
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "deactivate_recipient_account":
      recipient = deactivate_recipient_account(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(
        recipient,
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "list_transfers":
      transfers = list_transfers(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(
        transfers,
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "cancel_transfer":
      transfer = cancel_transfer(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(
        transfer,
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "get_transfer_by_id":
      transfer = get_transfer_by_id(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(
        transfer,
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "list_profiles":
      profiles = list_profiles(self._api_client, self._context).to_dict()
      return json.dumps(
        profiles,
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "get_profile_by_id":
      profile = get_profile_by_id(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(
        profile,
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "get_quote_by_id":
      quote = get_quote_by_id(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(
        quote,
        default=str  # to_dict() does not serialize datetime objects
      )
    elif method == "get_recipient_account_by_id":
      recipient = get_recipient_account_by_id(self._api_client, self._context, *args, **kwargs).to_dict()
      return json.dumps(
        recipient,
        default=str  # to_dict() does not serialize datetime objects
      )
    else:
      raise ValueError("Invalid method " + method)
