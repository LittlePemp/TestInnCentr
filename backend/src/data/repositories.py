from datetime import datetime
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection
from src.models.entities import News
from src.utils.result import Result


class NewsRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def add(self, entity: News) -> Result[News]:
        try:
            news_dict = entity.__dict__.copy()
            news_dict['_id'] = news_dict.pop('id')

            await self.collection.insert_one(news_dict)
            return Result.Success(entity)
        except Exception as e:
            return Result.Error(str(e))

    async def get_latest_publication_date(self) -> Result[Optional[datetime]]:
        try:
            document = await self.collection.find_one(
                {},
                sort=[('publication_datetime', -1)]
            )
            if document:
                latest_date = document['publication_datetime']
                if isinstance(latest_date, datetime):
                    return Result.Success(latest_date)
            return Result.Success(None)
        except Exception as e:
            return Result.Error(str(e))

    async def get_news_between_dates(self, start_date: datetime, end_date: datetime) -> Result[list[News]]:
        try:
            cursor = self.collection.find({
                'publication_datetime': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }).sort('publication_datetime', -1)
            news_list = []
            async for document in cursor:
                news = News(
                    id=document['_id'],
                    title=document['title'],
                    image_url=document['image_url'],
                    publication_datetime=document['publication_datetime'],
                    parsed_at_utc=document['parsed_at_utc']
                )
                news_list.append(news)

            return Result.Success(news_list)
        except Exception as e:
            return Result.Error(str(e))
