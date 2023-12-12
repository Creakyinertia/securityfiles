from sqlalchemy import Boolean, Column, Integer, String

from .database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String)
    full_name=Column(String)
    email=Column(String)
    hashed_password=Column(String)
    disabled=Boolean