from decimal import Decimal

from pydantic import BaseModel, Field


class OrderItemInput(BaseModel):
    sku: str = Field(min_length=1, examples=["SKU-APPLE"])
    quantity: int = Field(gt=0, examples=[1])
    unit_price: Decimal = Field(gt=0, examples=[120])


class PlaceOrderRequest(BaseModel):
    customer_id: str = Field(min_length=1, examples=["customer-001"])
    items: list[OrderItemInput] = Field(min_length=1)
    currency: str = Field(min_length=3, max_length=3, examples=["JPY"])


class PlaceOrderResult(BaseModel):
    order_id: str
    status: str
    charged: Decimal
