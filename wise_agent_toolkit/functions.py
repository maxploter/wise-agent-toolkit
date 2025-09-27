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
          api_client: The Wise API client.
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

  # Create TransferDetails object using Python field names
  transfer_details = wise_api_client.TransferDetails(
    reference=reference,
    transfer_purpose=transfer_purpose,
    transfer_purpose_sub_transfer_purpose=transfer_purpose_sub,
    transfer_purpose_invoice_number=transfer_purpose_invoice,
    source_of_funds=source_of_funds
  )

  # Create CreateStandardTransferRequest object using Python field names
  create_standard_transfer_request = wise_api_client.CreateStandardTransferRequest(
    target_account=int(recipient_id),
    quote_uuid=quote_id,
    customer_transaction_id=customer_transaction_id,
    details=transfer_details
  )

  return transfer_api.create_transfer(create_standard_transfer_request)


def create_quote(
  api_client,
  context: Context,
  source_currency: str,
  target_currency: str,
  source_amount: Optional[float] = None,
  target_amount: Optional[float] = None,
  profile_id: Optional[str] = None,
  pay_out: Optional[str] = None,
  preferred_pay_in: Optional[str] = None,
):
  """
  Create a quote.

  Parameters:
      api_client: The Wise API client.
      context (Context): The context.
      source_currency (str): The source currency code.
      target_currency (str): The target currency code.
      source_amount (float, optional): The source amount.
      target_amount (float, optional): The target amount.
      profile_id (str, optional): The profile ID. If not provided, will be taken from context.
      pay_out (str, optional): The pay out method.
      preferred_pay_in (str, optional): The preferred pay in method.

  Returns:
      The created quote.
  """
  quotes_api = wise_api_client.QuotesApi(api_client)

  # Get profile ID from context if not provided
  if not profile_id:
    profile_id = context.get("profile_id")
    if not profile_id:
      raise ValueError("Profile ID must be provided either as a parameter or in context.")

  # Either source_amount or target_amount should be provided, but not both
  if source_amount is not None and target_amount is not None:
    raise ValueError("Please provide either source_amount or target_amount, not both.")
  elif source_amount is None and target_amount is None:
    raise ValueError("Either source_amount or target_amount must be provided.")

  # Create payment metadata if pay_out or preferred_pay_in are provided
  payment_metadata = None
  if pay_out or preferred_pay_in:
    payment_metadata = wise_api_client.CreateAuthenticatedQuoteRequestBasePaymentMetadata(
      pay_out=pay_out,
      preferred_pay_in=preferred_pay_in
    )

  # Create the appropriate request object based on which amount is provided
  if source_amount is not None:
    # Use CreateAuthenticatedSourceAmountQuoteRequest
    quote_request = wise_api_client.CreateAuthenticatedSourceAmountQuoteRequest(
      sourceCurrency=source_currency,
      targetCurrency=target_currency,
      sourceAmount=source_amount,
      paymentMetadata=payment_metadata
    )
  else:
    # Use CreateAuthenticatedTargetAmountQuoteRequest
    quote_request = wise_api_client.CreateAuthenticatedTargetAmountQuoteRequest(
      sourceCurrency=source_currency,
      targetCurrency=target_currency,
      targetAmount=target_amount,
      paymentMetadata=payment_metadata
    )

  # Create the main request object
  create_authenticated_quote_request = wise_api_client.CreateAuthenticatedQuoteRequest(quote_request)

  # Make the API call
  return quotes_api.create_authenticated_quote(int(profile_id), create_authenticated_quote_request)


def create_recipient_account(
  api_client,
  context: Context,
  account_holder_name: str,
  currency: str,
  type: str,
  profile_id: Optional[int] = None,
  owned_by_customer: Optional[bool] = None,
  **kwargs
):
  """
  Create a recipient account.

  Parameters:
      api_client: The Wise API client.
      context (Context): The context.
      account_holder_name (str): The name of the account holder.
      currency (str): The currency code (3-letter ISO currency code).
      type (str): The type of recipient account.
      profile_id (int, optional): The profile ID. If not provided, will be taken from context.
      owned_by_customer (bool, optional): Whether this account is owned by the sending user.
      **kwargs: Dynamic fields based on account requirements (e.g., details, address, etc.).

  Returns:
      Recipient: The created recipient account.
  """
  recipients_api = wise_api_client.RecipientsApi(api_client)

  # Get profile ID from context if not provided
  if profile_id is None:
    profile_id = context.get("profile_id")
    if not profile_id:
      raise ValueError("Profile ID must be provided either as a parameter or in context.")

  # Create the request dictionary with fixed fields
  create_recipient_request_dict = {
    "accountHolderName": account_holder_name,
    "currency": currency,
    "type": type,
    "profile": int(profile_id)
  }

  # Add optional fixed field
  if owned_by_customer is not None:
    create_recipient_request_dict["ownedByCustomer"] = owned_by_customer

  # Add all dynamic fields
  create_recipient_request_dict.update(kwargs)

  # Create the request object from dictionary
  create_recipient_request = wise_api_client.CreateRecipientRequest.from_dict(create_recipient_request_dict)

  # Make the API call
  return recipients_api.create_recipient_account(create_recipient_request)


def list_recipient_accounts(
  api_client,
  context: Context,
  profile_id: Optional[str] = None,
  currency: Optional[str] = None,
  size: Optional[int] = None,
  seek_position: Optional[int] = None,
):
  """
  List recipient accounts.

  Parameters:
      api_client: The Wise API client.
      context (Context): The context.
      profile_id (str, optional): The profile ID. If not provided, will be taken from context.
      currency (str, optional): Filter by currency.
      size (int, optional): Number of items per page.
      seek_position (int, optional): Position to start seeking from.

  Returns:
      PaginatedRecipients: A paginated list of recipient accounts.
  """
  recipients_api = wise_api_client.RecipientsApi(api_client)

  # Get profile ID from context if not provided
  if not profile_id:
    profile_id = context.get("profile_id")
    if not profile_id:
      raise ValueError("Profile ID must be provided either as a parameter or in context.")

  # Make the API call
  return recipients_api.list_recipient_accounts(
    profile_id=int(profile_id),
    currency=currency,
    size=size,
    seek_position=seek_position
  )
