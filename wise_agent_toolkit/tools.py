from typing import Dict, List

from .prompts import (
    CREATE_TRANSFER_PROMPT, CREATE_QUOTE_PROMPT,
)

from .schema import (
    CreateTransfer, CreateQuote,
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
]
