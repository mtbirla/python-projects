from fastapi import Depends

from TodoApp.dependencies.repositories import get_todo_repository, get_user_repository
from TodoApp.Respositories.TodoRepository import TodoRepository
from TodoApp.Respositories.UserRepository import UserRepository

from TodoApp.services.TodoService import TodoService
from TodoApp.services.AuthService import AuthService
from TodoApp.services.UserService import UserService

from TodoApp.authorization.authDependency import AuthDependency

def get_todo_service(repo: TodoRepository[Depends(get_todo_repository)]):
    return TodoService(repo)

def get_auth_dependency(repo: UserRepository[Depends(get_user_repository)]):
    return AuthDependency(repo)

def get_auth_service(repo: UserRepository[Depends(get_user_repository)]):
    return AuthService(repo, get_auth_dependency(repo))

def get_user_service(repo: UserRepository[Depends(get_user_repository)]):
    return UserService(repo)