from pydantic import BaseModel

class Food(BaseModel):
    fname: str
    image: str
    category: str
    price: float
