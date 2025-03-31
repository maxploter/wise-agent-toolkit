CREATE_TRANSFER_PROMPT = """
This tool will create a transfer between accounts in Wise.

It takes the following arguments:
- recipient_id (str): The ID of the recipient (target account).
- quote_id (str): The ID of the quote (quote UUID).
- reference (str): Reference for the transfer (required, max 100 chars).
- customer_transaction_id (str, optional): A unique ID for this transaction. If not provided, a UUID will be generated.
- transfer_purpose (str, optional): Purpose of the transfer.
- transfer_purpose_sub (str, optional): Sub-purpose of the transfer.
- transfer_purpose_invoice (str, optional): Invoice number related to the transfer.
- source_of_funds (str, optional): Source of funds for the transfer.

Returns:
    The created transfer object from Wise.
"""
