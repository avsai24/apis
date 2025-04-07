from fastapi import FastAPI
from task_routes import router  

app = FastAPI()

app.include_router(router) 