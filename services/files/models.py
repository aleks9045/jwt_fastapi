from sqlalchemy import Column, MetaData, Integer, String, ForeignKey

from backend.database import Base

metadata = MetaData()


class FileModel(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)

