from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from src.utils.result import Result

from .errors import EntitiesErrorMessages


@dataclass
class News:
    id: str
    title: str
    image_url: str
    publication_datetime: datetime
    parsed_at_utc: datetime

    @staticmethod
    def create(title: str,
               image_url: str,
               publication_datetime: datetime,
               parsed_at_utc: datetime | None = None) -> Result['News']:
        try:
            # TODO: Params can be validated
            if not parsed_at_utc:
                parsed_at_utc = datetime.now(timezone.utc)

            news = News(
                id=str(uuid4()),
                title=title,
                image_url=image_url,
                publication_datetime=publication_datetime,
                parsed_at_utc=parsed_at_utc
            )
            return Result.Success(news)
        except Exception as _:
            return Result.Error(EntitiesErrorMessages.error_creating_news())
