from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, instance):
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
