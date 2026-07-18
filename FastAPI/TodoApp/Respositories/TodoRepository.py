from sqlalchemy import select, Delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import Todo
from fastapi import HTTPException

class TodoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Todo))
        return result.scalars().all()

    async def get_todo_by_id(self, todoId: int):
        result = await self.db.execute(
            select(Todo).where(Todo.id == todoId)
        )
        return result.scalar_one_or_none()

    async def create_todo(self, todoRequest: Todo):
        self.db.add(todoRequest)
        await self.db.commit()
        await self.db.refresh()

    async def update_todo(self, todoRequest: Todo):
        result = await self.db.execute(
            select(Todo).where(Todo.id == todoRequest.id)
        )
        db_todo = result.scalar_one_or_none()
        if db_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
            
        db_todo.title = todoRequest.title
        db_todo.description = todoRequest.description
        db_todo.priority = todoRequest.priority
        db_todo.completed = todoRequest.completed
        self.db.add(db_todo)
        await self.db.commit()
        await self.db.refresh()

    async def delete_todo(self, todoId: int):
        await self.db.execute(Delete(Todo).where(Todo.id == todoId))