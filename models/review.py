from pydantic import BaseModel
import datetime
from db import conn
from schemas.user import userEntity
from models.user import User
from bson import ObjectId

class Review(BaseModel):
    f_id: str
    user: dict
    content: str
    time: str
    def getUser(self):
        return userEntity(
            conn.foodsell.users.find_one({"_id": ObjectId(self.u_id)})
            )