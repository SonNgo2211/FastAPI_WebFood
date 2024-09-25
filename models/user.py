
from sqlalchemy import Table, Boolean, Column, Integer, String
from db import Base
from pydantic import BaseModel

class Config:
    arbitrary_types_allowed = True

class User(BaseModel):
    id: int
    fullname: str
    username: str
    email: str
    password: str

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key= True, index=True)
    fullname = Column(String(200))
    username = Column(String(100), unique=True, index=True)
    email =  Column(String(100), unique=True, index=True)
    password = Column(String(250))


