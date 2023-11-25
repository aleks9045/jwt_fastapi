from sqlalchemy import Column, Integer, String, ForeignKey

from backend.database import Base


class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String(32), nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    photo = Column(String, nullable=True)
