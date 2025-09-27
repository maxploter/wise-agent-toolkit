from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class CreateTransfer(BaseModel):
    """Schema for the ``create_transfer`` operation."""

    target_account: int = Field(
        ...,
        description="The ID of the target recipient account.",
    )

    quote_uuid: str = Field(
        ...,
        description="The UUID of the quote.",
    )

    reference: Optional[str] = Field(
        None,
        description="Reference for the transfer (optional, max 100 chars).",
    )

    source_account: Optional[int] = Field(
        None,
        description="The ID of the source account (for refunds).",
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

    target_account: Optional[int] = Field(
        None,
        description="A unique recipient account identifier.",
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

class ListRecipientAccounts(BaseModel):
    """Schema for the ``list_recipient_accounts`` operation."""

    profile_id: Optional[str] = Field(
        None,
        description="The profile ID to list recipients for. If not provided, will be taken from context.",
    )

    currency: Optional[str] = Field(
        None,
        description="Filter recipients by currency (3-letter ISO currency code).",
    )

    size: Optional[int] = Field(
        None,
        description="Number of items per page for pagination.",
    )

    seek_position: Optional[int] = Field(
        None,
        description="Position to start seeking from for pagination.",
    )

class CreateRecipientAccount(BaseModel):
    """Schema for the ``create_recipient_account`` operation."""

    account_holder_name: str = Field(
        ...,
        description="The recipient's full name.",
    )

    currency: str = Field(
        ...,
        description="3 character currency code for the recipient's account.",
    )

    type: str = Field(
        ...,
        description="The type of recipient account, determined from the account requirements.",
    )

    profile_id: Optional[int] = Field(
        None,
        description="The profile ID that the recipient will be created under. If not provided, will be taken from context.",
    )

    owned_by_customer: Optional[bool] = Field(
        None,
        description="Whether this account is owned by the sending user.",
    )

    class Config:
        extra = "allow"  # Allow additional fields for dynamic properties