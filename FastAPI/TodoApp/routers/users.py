from fastapi import APIRouter, Depends, HTTPException
from models import Users
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from TodoApp.authorization.authDependency import AuthDependency
from TodoApp.services.UserService import UserService
from TodoApp.dependencies.services import get_user_service

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=50)
    priority: int = Field(gt=0, lt=6)
    completed: bool

router = APIRouter(
    prefix='/users',
    tags=['users']
)

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

usrService_dependency = Annotated[UserService, Depends(get_user_service)]
user_dependency = Annotated[dict, Depends(AuthDependency.get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(usr: user_dependency, srvc: usrService_dependency):
    if usr is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return await srvc.get_user_by_id(usr.get('id'))

@router.put('/change-password', status_code=status.HTTP_202_ACCEPTED)
async def change_password(usr: user_dependency, srvc: usrService_dependency, userModel: UserVerification):
    if usr is None:
        return HTTPException(status_code=401, detail='Authentication failed')

    return await srvc.update_Password(usr.get('id'), userModel.new_password)