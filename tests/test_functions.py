import unittest
from unittest import mock

from wise_agent_toolkit.functions import create_transfer, create_quote


class TestWiseFunctions(unittest.TestCase):

    def test_create_transfer(self):
        mock_api_client = mock.Mock()
        mock_transfer_api = mock.Mock()
        mock_response = {"id": "123", "status": "pending"}

        with mock.patch("wise_api_client.TransfersApi") as mock_transfers_api_class:
            mock_transfers_api_class.return_value = mock_transfer_api
            mock_transfer_api.v1_transfers_post.return_value = mock_response

            context = {"account": "test-account"}
            recipient_id = "12345"
            quote_id = "quote-uuid-123"
            reference = "Test Payment"

            result = create_transfer(
                api_client=mock_api_client,
                context=context,
                recipient_id=recipient_id,
                quote_id=quote_id,
                reference=reference
            )

            mock_transfers_api_class.assert_called_once_with(mock_api_client)

            mock_transfer_api.v1_transfers_post.assert_called_once()

            call_args = mock_transfer_api.v1_transfers_post.call_args[0][0]

            self.assertEqual(int(recipient_id), call_args.target_account)
            self.assertEqual(quote_id, call_args.quote_uuid)
            self.assertEqual(reference, call_args.details.reference)

            self.assertEqual(result, mock_response)

    def test_create_quote(self):
        mock_api_client = mock.Mock()
        mock_quotes_api = mock.Mock()
        mock_response = {"id": "quote-123", "rate": 1.2, "sourceAmount": 100, "targetAmount": 120}

        with mock.patch("wise_api_client.QuotesApi") as mock_quotes_api_class:
            mock_quotes_api_class.return_value = mock_quotes_api
            mock_quotes_api.v3_profiles_profile_id_quotes_post.return_value = mock_response

            # Test with source_amount
            context = {"profile_id": "456"}
            source_currency = "USD"
            target_currency = "EUR"
            source_amount = 100

            result = create_quote(
                api_client=mock_api_client,
                context=context,
                source_currency=source_currency,
                target_currency=target_currency,
                source_amount=source_amount
            )

            mock_quotes_api_class.assert_called_once_with(mock_api_client)
            mock_quotes_api.v3_profiles_profile_id_quotes_post.assert_called_once()

            call_args = mock_quotes_api.v3_profiles_profile_id_quotes_post.call_args
            self.assertEqual(int(context["profile_id"]), call_args[0][0])  # profile_id
            self.assertEqual(source_currency, call_args[0][1].source_currency)
            self.assertEqual(target_currency, call_args[0][1].target_currency)
            self.assertEqual(source_amount, call_args[0][1].source_amount)
            self.assertIsNone(call_args[0][1].target_amount)

            self.assertEqual(result, mock_response)


if __name__ == "__main__":
    unittest.main()