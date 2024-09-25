from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import SessionLocal
from models.user import User
from fastapi import Depends

# Kết nối với database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Review(BaseModel):
    f_id: str
    user_id: int
    content: str
    time: str

    def getUser(self, db: Session):
        return db.query(User).filter(User.id == self.user_id).first()
