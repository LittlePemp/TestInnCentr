# Тестовое задание для Иннфовационный Центр "Безопасный Транспорт"
## ТЗ
Написать API, которое получает новости за заданный период из базы
и парсер который каждые 10 минут парсит новости
с сайта http://mosday.ru/news/tags.php?metro
(достаточно будет просто взять те новости что есть
при первой загрузке)
и сохраняет в базу с меткой когда эти новости спаршены,
пример метода
/metro/news?day=5
в качестве ответа вернуть JSON новости которые о
публикованы за последний 5 дней (включительно)

- заголовок
- url картинки
- дата публикации (YYYY-mm-dd)

что использовать
flask/fastapi, docker + любая база

## Используемые технологии
- Python 3.12
- FastAPI
- MongoDB
- Celery + Redis
- Docker

## Методы решения
### Парсинг
Был реализован сервис парсинга backend/src/services/parsing_service.py, который занимается получением объектов постов:

```python
from datetime import datetime
from pydantic import BaseModel

class News(BaseModel):
    id: str
    title: str
    image_url: str
    publication_datetime: datetime
    parsed_at_utc: datetime

```

Для получения html используется синхронный requests.

Для обработки html используется bs4. Определение элементов происходило по тегам и стилям css.

Получение актуальных постов происходит на основе сравнения дат публикаций.

### БД
Реализованы методы взаимодействия с БД (backend/src/data/repositories.py) для получения новостей в определенный промежуток времени, их добавление и получение последней даты публикации поста

### Шедулеры
Шедулер работает через Celery-Beat в Celery Worker. Запускается при инициализации docker-compose, чтобы база первоначально заполнилась.

## Запуск
1. Создать .env файл в корне проекта:
```bash
# FastAPI
APP_NAME=TestInnCentr
APP_ENV=development
APP_DEBUG=True
APP_HOST=0.0.0.0
APP_PORT=8000

# MongoDB
MONGODB_USER=mongodb_user
MONGODB_PASSWORD=password
MONGODB_DB=TestInnCentr
MONGODB_HOST=mongodb
MONGODB_PORT=27017

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

```
2. Запустить Docker-compose:
```bash
docker-compose up -d
```

3. Перейти на http://127.0.0.1:8000/docs и протестировать.


## Возможные
- Кастомные обработчики ошибок
- Логирование
- Тесты
