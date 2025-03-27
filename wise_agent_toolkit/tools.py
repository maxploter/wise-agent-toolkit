from typing import Dict, List

from .prompts import (
    CREATE_TRANSFER_PROMPT,
)

from .schema import (
    CreateTransfer,
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
]
