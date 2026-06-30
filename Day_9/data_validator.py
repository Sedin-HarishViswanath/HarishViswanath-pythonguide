"""
Day 9 — Assignment 2: Pydantic Data Validator — Food Order
Pydantic v2 • Field constraints • Enum • model_validator • ValidationError

NOTE on the starter code: it's written in Pydantic v1 syntax (@validator,
min_items). `pip install pydantic` today gives you v2 (2.13.x), which
renamed/changed these:
    v1                      ->  v2  
    @validator("field")     ->  @field_validator("field")
    Field(..., min_items=1) ->  Field(..., min_length=1)
    .dict() / .json()       ->  .model_dump() / .model_dump_json()

A second, more important fix: the starter's business-rule validator
    if sum(i.price * i.quantity for i in items) <= 0: raise ValueError(...)
can never actually fire. OrderItem already requires price > 0 (gt=0) and
quantity >= 1 (ge=1), and Order requires at least one item (min_length=1).
Sum of at least one positive number is always positive — it's dead code.
To make the business rule meaningful, this version adds a `discount`
field and checks the total *after* discount, which is the realistic
Swiggy/Zomato scenario (a coupon discount that exceeds the cart value).

Run: python3 assignment2.py
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class PaymentMethod(str, Enum):
    UPI = "upi"
    CARD = "card"
    CASH = "cash"


class OrderItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., ge=1, le=20)
    price: float = Field(..., gt=0)


class Order(BaseModel):
    customer_name: str = Field(..., min_length=2)
    items: List[OrderItem] = Field(..., min_length=1)  # v1: min_items=1
    delivery_address: str = Field(..., min_length=10)
    payment_method: PaymentMethod
    discount: float = Field(0.0, ge=0)
    tip: Optional[float] = Field(None, ge=0, le=500)


    @model_validator(mode="after")
    def total_must_be_positive(self) -> "Order":
        total = sum(i.price * i.quantity for i in self.items) - self.discount
        if total <= 0:
            raise ValueError(f"Order total must be > 0 after discount (got \u20b9{total:.2f})")
        return self

    @property
    def total(self) -> float:
        return sum(i.price * i.quantity for i in self.items) - self.discount


def print_errors(e: ValidationError) -> None:
    for err in e.errors():
        loc = ".".join(str(p) for p in err["loc"]) or "(root)"
        print(f"  field={loc!r:30} msg={err['msg']!r}")


def main() -> None:
    print("=== Valid order ===")
    good = Order(
        customer_name="Harish",
        items=[
            OrderItem(name="Paneer Butter Masala", quantity=2, price=220.0),
            OrderItem(name="Butter Naan", quantity=4, price=40.0),
        ],
        delivery_address="12 Anna Salai, Chennai, TN",
        payment_method=PaymentMethod.UPI,
        discount=50.0,
        tip=30.0,
    )
    print(good.model_dump_json(indent=2))
    print(f"  -> computed total: {good.total:.2f}")

    print("\n=== Invalid: field-level constraint violations ===")
    try:
        Order(
            customer_name="H",            # min_length=2 fails
            items=[],                     # min_length=1 fails
            delivery_address="short",     # min_length=10 fails
            payment_method="netbanking",  # not a valid enum member
            tip=1000,                     # le=500 fails
        )
    except ValidationError as e:
        print_errors(e.json(indent=4))

    print("\n=== Invalid: business rule (discount exceeds cart total) ===")
    try:
        Order(
            customer_name="Harish",
            items=[OrderItem(name="Masala Dosa", quantity=1, price=80.0)],
            delivery_address="12 Anna Salai, Chennai, TN",
            payment_method=PaymentMethod.CASH,
            discount=100.0,  # bigger than the 80.0 cart total
        )
    except ValidationError as e:
        print_errors(e.json(indent=4))

    print("\n=== Invalid: nested item constraint (quantity too high) ===")
    try:
        Order(
            customer_name="Harish",
            items=[OrderItem(name="Idli", quantity=50, price=10.0)],  # le=20 fails
            delivery_address="12 Anna Salai, Chennai, TN",
            payment_method=PaymentMethod.UPI,
        )
    except ValidationError as e:
        print_errors(e.json(indent=4))


if __name__ == "__main__":
    main()