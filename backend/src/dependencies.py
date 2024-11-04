from typing import AsyncGenerator

from src.data.uow import UnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork() as uow:
        yield uow
