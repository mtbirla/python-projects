from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todo
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from TodoApp.services.TodoService import TodoService
from TodoApp.dependencies.services import get_todo_service
from TodoApp.authorization.authDependency import AuthDependency

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5)
    priority: int = Field(gt=0, lt=6)
    completed: bool

router = APIRouter()

user_dependency = Annotated[dict, Depends(AuthDependency.get_current_user)]
todoService_dependency = Annotated[TodoService, Depends(get_todo_service)]

@router.get("/")
async def read_all(usr: user_dependency, service: todoService_dependency):
    return await service.get_all()

@router.get("/todo/{id}", status_code= status.HTTP_200_OK)
async def read_todo_by_id(usr: user_dependency, service: todoService_dependency, id: int = Path(gt=0)):
    if usr is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to access this resource')

    todo_data = await service.get_by_id(id)
    if todo_data is not None:
        return todo_data
    raise HTTPException(status_code = 404, detail="No todo found")

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(usr: user_dependency, service: todoService_dependency, todo_req:TodoRequest):
    if usr is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to access this resource')

    todo_model = Todo(**todo_req.dict(), owner_id = usr.get('id'))
    await service.create_todo(todo_model)

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(usr:user_dependency, service: todoService_dependency, todo_req:TodoRequest, todo_id:int = Path(gt=0)):
    if usr is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to access this resource')
    
    todo_data = Todo()

    todo_data.title = todo_req.title
    todo_data.description = todo_req.description
    todo_data.priority = todo_req.priority
    todo_data.completed = todo_req.completed
    
    await service.update_todo(todo_data)

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(usr: user_dependency, service: todoService_dependency, todo_id: int = Path(gt=0)):
    if usr is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to access this resource')
    
    todo_data = await service.get_by_id(todo_id)

    if todo_data is None:
        raise HTTPException(status_code=404, detail="No todo found to delete")

    await service.delete_todo(todo_id)