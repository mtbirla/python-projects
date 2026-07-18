from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from TodoApp.Core.database import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session