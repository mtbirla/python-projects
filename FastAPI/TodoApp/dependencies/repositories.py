from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from TodoApp.db.dependencies import get_db
from TodoApp.Respositories.TodoRepository import TodoRepository
from TodoApp.Respositories.UserRepository import UserRepository

def get_todo_repository(db: AsyncSession[Depends(get_db)]):
    return TodoRepository(db)

def get_user_repository(db: AsyncSession[Depends(get_db)]):
    return UserRepository(db)