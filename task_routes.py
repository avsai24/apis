from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task, TaskDB, UserCreate, UserOut, UserDB
from auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    return db.query(TaskDB).filter(TaskDB.user_id == current_user.id).all()

@router.post("/tasks")
def create_task(task: Task, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    new_task = TaskDB(
        title=task.title,
        completed=task.completed,
        user_id=current_user.id 
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        task.title = updated_task.title
        task.completed = updated_task.completed
        db.commit()
        db.refresh(task)
        return task
    return {"error": "Task not found"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": f"Task with id {task_id} deleted"}
    return {"error": "Task not found"}

@router.post("/users/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    new_user = UserDB(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_tasks(db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    return db.query(TaskDB).all()

