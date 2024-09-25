from pydantic import BaseModel
from typing import Dict, List

class CartItem(BaseModel):
    f_id: str
    fname: str
    image: str
    price: float
    quantity: int

class Cart(BaseModel):
    u_id: str
    items: List[CartItem]
    amount: float
