from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todo
from sqlalchemy.orm import session
from database import SessionLocal
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5)
    priority: int = Field(gt=0, lt=6)
    completed: bool

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/")
async def read_all(usr: user_dependency, db: db_dependency):
    return db.query(Todo).filter(Todo.owner_id == usr.get('userId')).all()

@router.get("/todo/{id}", status_code= status.HTTP_200_OK)
async def read_todo_by_id(usr: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    if usr is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to access this resource')

    todo_data = db.query(Todo).filter(Todo.owner_id == usr.get('userId'),
                                     Todo.id == id).first()
    if todo_data is not None:
        return todo_data
    raise HTTPException(status_code = 404, detail="No todo found")

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(usr: user_dependency, db: db_dependency, todo_req:TodoRequest):
    if usr is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to access this resource')

    todo_model = Todo(**todo_req.dict(), owner_id = usr.get('userId'))
    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(usr:user_dependency, db:db_dependency, todo_req:TodoRequest, todo_id:int = Path(gt=0)):
    if usr is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to access this resource')
    
    todo_data = db.query(Todo).filter(Todo.owner_id == usr.get('userId'),
                                     Todo.id == todo_id).first()

    if todo_data is None:
        raise HTTPException(status_code=404, detail="No todo found to update")

    todo_data.title = todo_req.title
    todo_data.description = todo_req.description
    todo_data.priority = todo_req.priority
    todo_data.completed = todo_req.completed
    db.add(todo_data)
    db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(usr: user_dependency, db:db_dependency, todo_id: int = Path(gt=0)):
    if usr is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to access this resource')
    
    todo_data = db.query(Todo).filter(Todo.owner_id == usr.get('userId'),
                                    Todo.id == todo_id).first()

    if todo_data is None:
        raise HTTPException(status_code=404, detail="No todo found to delete")

    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()