from models import Todo
from TodoApp.Respositories.TodoRepository import *

class TodoService:

    def __init__(self, repo: TodoRepository):
        self.repo = repo

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(self, todoId):
        return await self.repo.get_todo_by_id(self, todoId)

    async def create_todo(self, todo: Todo):
        return await self.repo.create_todo(todo)

    async def delete_todo(self, todoId: int):
        return await self.repo.delete_todo(todoId)

    async def update_todo(self, todo: Todo):
        return await self.repo.update_todo(todo)