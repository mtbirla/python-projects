from Core.database import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(DeclarativeBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_pwd = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)

class Todo(DeclarativeBase):
    __tablename__ = "todo"

    id = Column(Integer, primary_key= True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))