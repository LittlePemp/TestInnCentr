import asyncio
import logging
from datetime import datetime

from celery import shared_task
from src.data.uow import UnitOfWork
from src.services.parsing_service import ParsingService
from src.utils.result import Result

logger = logging.getLogger(__name__)

@shared_task(name='src.tasks.fetch_and_save_latest_news')
def fetch_and_save_latest_news():
    asyncio.run(_fetch_and_save_latest_news())

async def _fetch_and_save_latest_news():
    ps = ParsingService()

    async with UnitOfWork() as uow:
        # Last update
        latest_date_res = await uow.news_repository.get_latest_publication_date()

        last_parsed_at = latest_date_res.value if latest_date_res.value else datetime(1970, 1, 1)

        logger.info(f'Search by datetime: {last_parsed_at}')
        posts_res = ps.parse_latest_posts(last_parsed_at)

        if posts_res.is_success:
            for news in posts_res.value:
                add_result: Result = await uow.news_repository.add(news)
                if not add_result.is_success:
                    logger.error(f'Save error: {add_result.error}')
                else:
                    logger.info(f'News saved: {add_result.value}')
        else:
            logger.error(f'Parsing error: {posts_res.error}')
