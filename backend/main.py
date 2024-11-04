import uvicorn
from fastapi import FastAPI
from settings import settings
from src.routers.news import router as news_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug
)

# Routes
app.include_router(news_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.app_host, port=settings.app_port, reload=True)
