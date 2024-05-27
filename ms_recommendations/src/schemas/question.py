from typing import Optional
from pydantic import Field
from schemas.base import BaseSchema


class CreatedQuestion(BaseSchema):
    """
    Модель вопроса
    """
    
    id: int = Field(title="Порядковый номер вопроса", ge=0)
    name: str = Field(title="Заголовок вопроса", min_length=5, max_length=256)
    description: Optional[str] = Field(title="Описание вопроса", default=None)