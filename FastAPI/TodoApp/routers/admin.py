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
    description: str = Field(min_length=5, max_length=50)
    priority: int = Field(gt=0, lt=6)
    completed: bool

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/todo', status_code=status.HTTP_200_OK)
def read_all(usr: user_dependency, db: db_dependency):
    if usr is None or usr.get('role')!='admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Todo).all()