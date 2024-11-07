import uuid
from datetime import datetime
from typing import List
import math
from pydantic import BaseModel, Field, validator

class Item(BaseModel):
    shortDescription: str = Field(..., description="A brief description of the item.")
    price: float = Field(..., description="Price of the item.")

    @validator('shortDescription')
    def description_must_not_be_empty(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Item description cannot be empty or whitespace.")
        return value

class Receipt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the receipt.")
    retailer: str = Field(..., description="Name of the retailer.")
    purchaseDate: str = Field(..., description="Date of purchase in YYYY-MM-DD format.")
    purchaseTime: str = Field(..., description="Time of purchase in HH:MM format.")
    items: List[Item] = Field(..., description="List of purchased items.")
    total: float = Field(..., description="Total amount spent.")
    points: int = Field(default=0, description="Points earned for the receipt.")

    @validator('purchaseDate')
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("purchaseDate must be in YYYY-MM-DD format.")
        return value

    @validator('purchaseTime')
    def validate_time(cls, value):
        try:
            datetime.strptime(value, "%H:%M")
        except ValueError:
            raise ValueError("purchaseTime must be in HH:MM format.")
        return value

    @validator('total')
    def validate_total(cls, value, values):
        item_total = sum(item.price for item in values.get('items', []))
        # Round both values to 2 decimal places before comparing
        if round(item_total, 2) != round(value, 2):
            raise ValueError(f"The total ({value}) does not match the sum of item prices ({item_total}).")
        return value

    @validator('points', always=True)
    def calculate_points(cls, value, values):
        try:
            retailer = values.get('retailer', '')
            total = values.get('total', 0.0)
            items = values.get('items', [])
            purchase_date = values.get('purchaseDate', '')
            purchase_time = values.get('purchaseTime', '')

            points = 0

            # One point for every alphanumeric character in the retailer name.
            points += sum(c.isalnum() for c in retailer)

            # 50 points if the total is a round dollar amount with no cents.
            if total == int(total):
                points += 50

            # 25 points if the total is a multiple of 0.25.
            if total % 0.25 == 0:
                points += 25

            # 5 points for every two items on the receipt.
            points += (len(items) // 2) * 5

            # Points for item descriptions (multiple of 3 condition).
            for item in items:
                if len(item.shortDescription.strip()) % 3 == 0:
                    points += math.ceil(item.price * 0.2)

            # 6 points if the day in the purchase date is odd.
            purchase_day = int(purchase_date.split('-')[2])  # Extracting day part from the date
            if purchase_day % 2 != 0:
                points += 6

            # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
            purchase_hour = int(purchase_time.split(':')[0])
            if 14 <= purchase_hour < 16:
                points += 10

            return points
        except Exception as e:
            raise ValueError(f"Error calculating points: {e}")
