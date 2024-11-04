from typing import Optional

from pydantic import BaseModel, Field


class NewsResponse(BaseModel):
    title: str = Field(..., description='Заголовок новости')
    image_url: Optional[str] = Field(None, description='URL картинка')
    publication_date: str = Field(..., description='Дата публикации (YYYY-mm-dd)')
