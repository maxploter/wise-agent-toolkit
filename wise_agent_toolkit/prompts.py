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

CREATE_QUOTE_PROMPT = """
This tool will create a quote for currency conversion in Wise.

It takes the following arguments:
- source_currency (str): The source currency code (3-letter ISO currency code).
- target_currency (str): The target currency code (3-letter ISO currency code).
- source_amount (float, optional): The amount in the source currency to be converted.
- target_amount (float, optional): The amount in the target currency to receive.
  Note: Provide either source_amount or target_amount, not both.
- profile_id (str, optional): The profile ID. If not provided, will be taken from context.
- pay_out (str, optional): The pay out method.
- preferred_pay_in (str, optional): The preferred pay in method.

Returns:
    The created quote object from Wise.
"""