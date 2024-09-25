from pydantic import BaseModel
from sqlalchemy import Table, Boolean, Column, Integer, String, Float
from db import Base

class Food(BaseModel):
    id: int
    fname: str
    image: str
    category: str
    price: str

class FoodModel(Base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key= True, index=True)
    fname = Column(String(100))
    image = Column(String(250))
    category = Column(String(100))
    price = Column(Float)
