from sqlalchemy import Column, Integer, String

from database import Base


class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(32), nullable=False, unique=True)
    hashed_password = Column(String(1023), nullable=False)
    photo = Column(String(255), nullable=True)
