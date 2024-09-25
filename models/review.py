from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, Session
from db import Base
from db import SessionLocal
from models.user import User, UserModel
from fastapi import Depends
from db import get_db


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key= True, index=True)
    f_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)
    time = Column(String(50))

    user = relationship("UserModel")

    def getUser(self, db: Session=Depends(get_db)):
        return db.query(UserModel).filter(UserModel.id == self.user_id).first()
