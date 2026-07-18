from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from starlette import status
from TodoApp.services.TodoService import TodoService
from TodoApp.dependencies.services import get_todo_service
from TodoApp.authorization.authDependency import AuthDependency

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

user_dependency = Annotated[dict, Depends(AuthDependency.get_current_user)]
todoService_dependency = Annotated[TodoService, Depends(get_todo_service)]

@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all(usr: user_dependency, service: todoService_dependency):
    if usr is None or usr.get('role')!='admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    return await service.get_all()