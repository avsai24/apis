from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from database import Base 

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

class Task(BaseModel):
    title: str
    completed: bool = False

    model_config = {
        "from_attributes": True
    }