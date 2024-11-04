from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from src.data.uow import UnitOfWork
from src.dependencies import get_uow
from src.models.entities import News
from src.schemas.news import NewsResponse
from src.utils.result import Result

router = APIRouter()

@router.get('/metro/news', response_model=list[NewsResponse])
async def get_news_last_days(day: int = Query(..., ge=1, description='Дней для последних новостей'),
                             uow: UnitOfWork = Depends(get_uow)):
    '''
    Возвращает список новостей за последние day дней
    '''
    try:
        # Date range before day
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=day)

        # Get News
        news_list_res: Result[list[News]] = await uow.news_repository.get_news_between_dates(start_date, end_date)

        if not news_list_res.is_success:
            raise HTTPException(status_code=500, detail=f'Ошибка при получении новостей: {news_list_res.error}')

        news_list: list[News] = news_list_res.value
        if not news_list:
            return []

        # Response
        response = [
            NewsResponse(
                title=news.title,
                image_url=news.image_url,
                publication_date=news.publication_datetime.strftime('%Y-%m-%d')
            )
            for news in news_list
        ]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
