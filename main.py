from fastapi import FastAPI
from task_routes import router
from database import Base, engine
from models import TaskDB 

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)