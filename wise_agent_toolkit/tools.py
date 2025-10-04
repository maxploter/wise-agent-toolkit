from typing import Dict, List

from .prompts import (
    CREATE_TRANSFER_PROMPT, CREATE_QUOTE_PROMPT, LIST_RECIPIENT_ACCOUNTS_PROMPT, CREATE_RECIPIENT_ACCOUNT_PROMPT, LIST_TRANSFERS_PROMPT,
)

from .schema import (
    CreateTransfer, CreateQuote, ListRecipientAccounts, CreateRecipientAccount, ListTransfers,
)

tools: List[Dict] = [
    {
        "method": "create_transfer",
        "name": "Create Transfer",
        "description": CREATE_TRANSFER_PROMPT,
        "args_schema": CreateTransfer,
        "actions": {
            "transfers": {
                "create": True,
            }
        },
    },
    {
        "method": "create_quote",
        "name": "Create Quote",
        "description": CREATE_QUOTE_PROMPT,
        "args_schema": CreateQuote,
        "actions": {
            "quotes": {
                "create": True,
            }
        },
    },
    {
        "method": "list_recipient_accounts",
        "name": "List Recipient Accounts",
        "description": LIST_RECIPIENT_ACCOUNTS_PROMPT,
        "args_schema": ListRecipientAccounts,
        "actions": {
            "recipients": {
                "read": True,
            }
        },
    },
    {
        "method": "create_recipient_account",
        "name": "Create Recipient Account",
        "description": CREATE_RECIPIENT_ACCOUNT_PROMPT,
        "args_schema": CreateRecipientAccount,
        "actions": {
            "recipients": {
                "create": True,
            }
        },
    },
    {
        "method": "list_transfers",
        "name": "List Transfers",
        "description": LIST_TRANSFERS_PROMPT,
        "args_schema": ListTransfers,
        "actions": {
            "transfers": {
                "read": True,
            }
        },
    },
]
