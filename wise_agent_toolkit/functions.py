from typing import Optional

import wise_api_client

from .configuration import Context


def create_transfer(
        api_client,
        context: Context,
        recipient_id: str,
        quote_id: str,
        reference: str,
        customer_transaction_id: Optional[str] = None,
        transfer_purpose: Optional[str] = None,
        transfer_purpose_sub: Optional[str] = None,
        transfer_purpose_invoice: Optional[str] = None,
        source_of_funds: Optional[str] = None
):
    """
    Create a transfer.

    Parameters:
            client: The Wise API client.
            context (Context): The context.
            recipient_id (str): The ID of the recipient (target account).
            quote_id (str): The ID of the quote (quote UUID).
            reference (str): Reference for the transfer (required).
            customer_transaction_id (str, optional): Customer transaction ID.
            transfer_purpose (str, optional): Purpose of the transfer.
            transfer_purpose_sub (str, optional): Sub-purpose of the transfer.
            transfer_purpose_invoice (str, optional): Invoice number.
            source_of_funds (str, optional): Source of funds.

    Returns:
            The created transfer.
    """
    transfer_api = wise_api_client.TransfersApi(api_client)

    if not customer_transaction_id:
        import uuid
        customer_transaction_id = str(uuid.uuid4())

    details_dict = {
        "reference": reference
    }

    if transfer_purpose:
        details_dict["transferPurpose"] = transfer_purpose
    if transfer_purpose_sub:
        details_dict["transferPurposeSubTransferPurpose"] = transfer_purpose_sub
    if transfer_purpose_invoice:
        details_dict["transferPurposeInvoiceNumber"] = transfer_purpose_invoice
    if source_of_funds:
        details_dict["sourceOfFunds"] = source_of_funds

    # Create main request dictionary
    transfer_request_dict = {
        "targetAccount": int(recipient_id),
        "quoteUuid": quote_id,
        "customerTransactionId": customer_transaction_id,
        "details": details_dict
    }

    transfer_data: dict = {
        "recipient_id": recipient_id,
        "quote_id": quote_id,
    }
    if context.get("account") is not None:
        account = context.get("account")
        if account is not None:
            transfer_data["wise_account"] = account

    create_standard_transfer_request = wise_api_client.CreateStandardTransferRequest.from_dict(transfer_request_dict)

    return transfer_api.v1_transfers_post(create_standard_transfer_request)
