from models import Users
from TodoApp.Respositories.UserRepository import UserRepository
from TodoApp.authorization.authDependency import AuthDependency

class AuthService:
    def __init__(self, repo: UserRepository, auth: AuthDependency):
        self.repo = repo
        self.auth = auth

    async def create_user(self, user: Users):
        return await self.repo.create_user(user)

    async def get_login_access_token(self, username: str, password: str) -> str:
        return await self.auth.get_access_token(username, password)