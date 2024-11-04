from motor.motor_asyncio import AsyncIOMotorClient
from settings import settings
from src.data.repositories import NewsRepository


class UnitOfWork:
    def __init__(self):
        mongo_uri = (
            f'mongodb://{settings.mongodb_user}:{settings.mongodb_password}'
            f'@{settings.mongodb_host}:{settings.mongodb_port}/'
            f'{settings.mongodb_db}?authSource=admin'
        )
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[settings.mongodb_db]

        # Repositories
        self.news_repository = NewsRepository(self.db['news'])

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
