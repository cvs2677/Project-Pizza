from typing import List, Optional

from pydantic import BaseModel

from app.db.models.user_model import PizzaSize


class PizzaCreate(BaseModel):
    name: str
    price: float
    size: PizzaSize

class PizzaOrder(BaseModel):
    pizza_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_id: int
    pizzas: List[PizzaOrder]

class PizzaOrderUpdate(BaseModel):
    pizza_id: int
    quantity: int

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    pizzas: Optional[List[PizzaOrderUpdate]] = None

