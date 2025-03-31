import unittest
from unittest import mock

from wise_agent_toolkit.functions import create_transfer


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