from TodoApp.Respositories.UserRepository import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def update_Password(self, userId: int, password: str):
        return await self.repo.update_user_password(password, userId)

    async def get_user_by_id(self, userId: int):
        return await self.repo.get_user_by_id(userId)