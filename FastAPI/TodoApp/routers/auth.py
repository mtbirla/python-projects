from fastapi import  APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import session
from database import SessionLocal
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '7b8d2f3c1e4a9f6d8c5b7a1e3f9d2c4b6e8f0a1c3d5e7f9b2a4c6d8e0f1a3b5'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, user_req: UserRequestModel):
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
    db.add(user_model)
    db.commit()


@router.post("/token", response_model= Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authneticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authrization failed')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'Bearer '}

def authneticate_user(username: str, password: str, db):
    user_data = db.query(Users).filter(Users.username == username).first()
    if user_data is None:
        return False
    if not bcrypt_context.verify(password, user_data.hashed_pwd):
        return False
    return user_data

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authrization failed')
        return {'username': username, 'userId': user_id, 'role': role }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authrization failed')