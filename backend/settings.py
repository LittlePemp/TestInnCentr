from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # FastAPI
    app_name: str = Field(..., env='APP_NAME')
    app_env: str = Field(..., env='APP_ENV')
    app_debug: bool = Field(..., env='APP_DEBUG')
    app_host: str = Field(..., env='APP_HOST')
    app_port: int = Field(..., env='APP_PORT')

    # MongoDB
    mongodb_user: str = Field(..., env='MONGODB_USER')
    mongodb_password: str = Field(..., env='MONGODB_PASSWORD')
    mongodb_db: str = Field(..., env='MONGODB_DB')
    mongodb_host: str = Field(default='127.0.0.1', env='MONGODB_HOST')
    mongodb_port: int = Field(..., env='MONGODB_PORT')

    # Redis
    redis_host: str = Field(default='127.0.0.1', env='REDIS_HOST')
    redis_port: str = Field(..., env='REDIS_PORT')

    model_config = SettingsConfigDict(
        env_file='../.env',
        env_file_encoding='utf-8'
    )

settings = Settings()
