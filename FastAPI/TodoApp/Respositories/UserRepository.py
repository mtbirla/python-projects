from sqlalchemy.ext.asyncio import AsyncSession
from models import Users
from passlib.context import CryptContext
from sqlalchemy import select
from fastapi import HTTPException

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

class UserRepository:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def create_user(self, user: Users):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh()

    async def get_user(self, username: str, password: str) -> Users:
        result = await self.db.execute(select(Users).where(Users.username == username))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=401, detail="User unauthorized")
        if not bcrypt_context.verify(password, user.hashed_pwd):
            raise HTTPException(status_code=401, detail="User unauthorized")
        return user

    async def update_user_password(self, password: str, userId: int):
        result = await self.db.execute(select(Users).where(Users.id == userId))
        usr = result.scalar_one_or_none()
        if usr is None:
            raise HTTPException(status_code=401, detail="Authentication failed")
        usr.hashed_pwd = password
        self.db.add(usr)
        await self.db.commit()

    async def get_user_by_id(self, userId: int):
        result = await self.db.execute(select(Users).where(Users.id == userId))
        return result.scalar_one_or_none()