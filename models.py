from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base 
from pydantic import BaseModel, EmailStr

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id")) 

class Task(BaseModel):
    title: str
    completed: bool = False

    model_config = {
        "from_attributes": True
    }

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True 
    }