from TodoApp.Respositories.UserRepository import *
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from fastapi import Depends
from typing import Annotated
from TodoApp.Core.config import get_settings

settings = get_settings()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class AuthDependency:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_access_token(self, username: str, password: str):
        user = self.repo.get_user(username, password)
        token = self.create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
        return {"access_token": token, "token_type": "Bearer"}

    async def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
        encode = {'sub': username, 'id': user_id, 'role': role}
        expires = datetime.now(timezone.utc) + expires_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get('sub')
            user_id: int = payload.get('id')
            role: str = payload.get('role')
            if username is None or user_id is None:
                raise HTTPException(status_code=401, detail='Authorization failed')
            return {'username': username, 'id': user_id, 'role': role }
        except JWTError:
            raise HTTPException(status_code=401, detail='Authorization failed')