from app.models import async_session
from app.models import AsyncSession


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
