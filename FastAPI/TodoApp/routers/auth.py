from fastapi import  APIRouter, Depends
from pydantic import BaseModel, Field
from TodoApp.dependencies.services import get_auth_service
from models import Users
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from TodoApp.services.AuthService import AuthService
from passlib.context import CryptContext

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRequestModel(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    pwd: str
    role: str
    phoneNumber: str = Field(min_length=10, max_length=11)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_req: UserRequestModel, service: Annotated[AuthService, Depends(get_auth_service)]):
    user_model = Users(
        email = user_req.email,
        username = user_req.username,
        first_name = user_req.first_name,
        last_name = user_req.last_name,
        role = user_req.role,
        is_active = True,
        hashed_pwd = bcrypt_context.hash(user_req.pwd),
        phone_number = user_req.phoneNumber
    )
    await service.create_user(user_model)


@router.post("/token", response_model= Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
        service: Annotated[AuthService, Depends(get_auth_service)]):
        return await service.get_login_access_token(form_data.username, form_data.password)