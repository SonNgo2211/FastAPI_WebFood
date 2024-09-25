
from pydantic import BaseModel, Field

class User(BaseModel):
    fullname: str
    username: str
    email: str
    password: str


