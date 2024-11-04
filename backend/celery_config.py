from celery import Celery
from settings import settings

# Celery Instance
celery_app = Celery(
    'news_parser',
    broker=f'redis://{settings.redis_host}:{settings.redis_port}/0',
    backend=f'redis://{settings.redis_host}:{settings.redis_port}/0',
    include=['src.tasks']
)

# Configure Celery
celery_app.conf.update(
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'fetch_and_save_latest_news': {
            'task': 'src.tasks.fetch_and_save_latest_news',
            'schedule': 600,  # 600
        },
    },
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    worker_pool='solo',  # Fix Windows
)

celery_app.autodiscover_tasks()
