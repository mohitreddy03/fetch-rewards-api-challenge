import unittest
import json
from uuid import uuid4
from app import create_app


class TestReceiptAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()  # Initialize the Flask app for testing
        self.client = self.app.test_client()
        self.valid_receipt_payload = {
            "retailer": "SuperMart",
            "purchaseDate": "2024-11-06",
            "purchaseTime": "15:30",
            "items": [
                {"shortDescription": "Apple", "price": 1.50},
                {"shortDescription": "Banana", "price": 0.75}
            ],
            "total": 2.25
        }

    def test_process_valid_receipt(self):
        """Test submitting a valid receipt."""
        response = self.client.post(
            '/v0/receipts/process',
            data=json.dumps(self.valid_receipt_payload),
            content_type='application/json'
        )
        print(response)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('id', response_data)  # Check if the response contains an 'id'
        self.receipt_id = response_data['id']  # Save the generated ID for other tests

    def test_get_points_for_valid_receipt(self):
        """Test retrieving points for an existing valid receipt."""
        # First, submit a valid receipt
        process_response = self.client.post(
            '/v0/receipts/process',
            data=json.dumps(self.valid_receipt_payload),
            content_type='application/json'
        )
        receipt_id = process_response.get_json().get('id')

        # Now, fetch the points for the submitted receipt
        points_response = self.client.get(f'/v0/receipts/{receipt_id}/points')
        self.assertEqual(points_response.status_code, 200)
        points_data = points_response.get_json()
        self.assertIn('points', points_data)  # Ensure the 'points' key is in the response
        self.assertGreaterEqual(points_data['points'], 0)  # Points should be zero or positive

    def test_process_invalid_receipt(self):
        """Test submitting an invalid receipt with missing fields."""
        invalid_payload = self.valid_receipt_payload.copy()
        del invalid_payload['retailer']  # Remove retailer field to make the payload invalid

        response = self.client.post(
            '/v0/receipts/process',
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_points_for_nonexistent_receipt(self):
        """Test retrieving points for a non-existent receipt ID."""
        fake_id = str(uuid4())  # Generate a random ID
        response = self.client.get(f'/receipts/{fake_id}/points')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
