from typing import Optional
from pydantic import BaseModel, Field


class CreateTransfer(BaseModel):
    """Schema for the ``create_transfer`` operation."""

    recipient_id: str = Field(
        ...,
        description="The ID of the recipient (target account).",
    )

    quote_id: str = Field(
        ...,
        description="The ID of the quote (quote UUID).",
    )

    reference: str = Field(
        ...,
        description="Reference for the transfer (required, max 100 chars).",
    )

    customer_transaction_id: Optional[str] = Field(
        None,
        description="A unique ID for this transaction. If not provided, a UUID will be generated.",
    )

    transfer_purpose: Optional[str] = Field(
        None,
        description="Purpose of the transfer.",
    )

    transfer_purpose_sub: Optional[str] = Field(
        None,
        description="Sub-purpose of the transfer.",
    )

    transfer_purpose_invoice: Optional[str] = Field(
        None,
        description="Invoice number related to the transfer.",
    )

    source_of_funds: Optional[str] = Field(
        None,
        description="Source of funds for the transfer.",
    )