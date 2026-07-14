from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todo, Users
from sqlalchemy.orm import session
from database import SessionLocal
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=50)
    priority: int = Field(gt=0, lt=6)
    completed: bool

class userUpdateRequest(BaseModel):
    phoneNumber: str = Field(min_length=10, max_length=10)

router = APIRouter(
    prefix='/users',
    tags=['users']
)

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

@router.get('/', status_code=status.HTTP_200_OK)
def get_user(usr: user_dependency, db: db_dependency):
    if usr is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Users).filter(Users.id == usr.get('userId')).first()

@router.put('/change-password', status_code=status.HTTP_202_ACCEPTED)
def change_password(usr: user_dependency, db: db_dependency, userModel: UserVerification):
    if usr is None:
        return HTTPException(status_code=401, detail='Authentication failed')
    usrModel = db.query(Users).filter(Users.id == usr.get('userId')).first()

    usrModel.hashed_pwd = bcrypt_context.hash(userModel.new_password)
    db.add(usrModel)
    db.commit()

@router.put('/update-user-number', status_code=status.HTTP_204_NO_CONTENT)
def update_user_number(usr: user_dependency, db: db_dependency, usr_update_model: userUpdateRequest):
    if usr is None:
        return HTTPException(status_code=401, detail='Authentication failed')
    usrModel = db.query(Users).filter(Users.id == usr.get('userId')).first()
    usrModel.phone_number = usr_update_model.phoneNumber
    db.add(usrModel)
    db.commit()