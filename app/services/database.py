from typing import Dict, Tuple, Union
from pydantic import ValidationError
from ..models.receipt import Receipt

class ReceiptDatabase:
    def __init__(self):
        self._receipts: Dict[str, Receipt] = {}

    def add_receipt(self, receipt_data: dict) -> Tuple[Union[Receipt, str], bool]:
        """Add a receipt and return a tuple indicating success and either the receipt or an error message."""
        try:
            receipt = Receipt(**receipt_data)
            self._receipts[receipt.id] = receipt
            return receipt, False
        except ValidationError as e:
            # Return False and the validation error message
            return e.json(), True

    def get_receipt(self, receipt_id: str) -> Tuple[Union[Receipt, str], bool]:
        """Retrieve a receipt by ID and return a tuple indicating success and either the receipt or an error message."""
        receipt = self._receipts.get(receipt_id)
        if receipt is None:
            return f"Receipt with ID {receipt_id} not found.", True
        return receipt, False

DB = ReceiptDatabase()