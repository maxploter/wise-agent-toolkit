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

class CreateQuote(BaseModel):
    """Schema for the ``create_quote`` operation."""

    source_currency: str = Field(
        ...,
        description="The source currency code (3-letter ISO currency code).",
    )

    target_currency: str = Field(
        ...,
        description="The target currency code (3-letter ISO currency code).",
    )

    source_amount: Optional[float] = Field(
        None,
        description="The amount in the source currency to be converted. Provide either source_amount or target_amount, not both.",
    )

    target_amount: Optional[float] = Field(
        None,
        description="The amount in the target currency to receive. Provide either source_amount or target_amount, not both.",
    )

    profile_id: Optional[str] = Field(
        None,
        description="The profile ID. If not provided, will be taken from context.",
    )

    pay_out: Optional[str] = Field(
        None,
        description="The pay out method.",
    )

    preferred_pay_in: Optional[str] = Field(
        None,
        description="The preferred pay in method.",
    )