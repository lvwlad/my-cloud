from sqlalchemy import Column, Integer, String, DATE, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase
#from database import Base
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String,  unique=True)
    user_name = Column(String)
    hash_password = Column(String)

    files = relationship("File", back_populates="user_id")

class File(Base):
    __tablename__ = "files"
    file_id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    is_folder = Column(Boolean)
    parrent_dir = Column(String)
    path = Column(String)
    upload_date = Column(DateTime)
    size = Column(Integer)
    owner = Column(Integer, ForeignKey('users.user_id'))

    user_id = relationship("User", back_populates="files")

class UserWithoutVerify(Base):
    __tablename__ = "users_without_verify"
    user_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String,  unique=True)
    user_name = Column(String)
    hash_password = Column(String)
    user_code = Column(String)


   

class Dirs(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    file_id : int
    filename : str
    is_folder: bool
    parrent_dir: Optional[str] = None
    path: str
    upload_date: Optional[datetime] = None
    size: int
    owner: int


class Uwv(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id : int
    user_email: str
    user_name:str
    user_code: str


class Us(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id : int
    user_email: str
    user_name:str




