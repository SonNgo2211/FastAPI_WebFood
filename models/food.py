from pydantic import BaseModel, Field

class Food(BaseModel):
    fname: str
    image: str
    category: str
    price: float
