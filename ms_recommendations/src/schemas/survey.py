from typing import Optional
from pydantic import Field
from schemas.base import BaseSchema
from schemas.base import BaseSchema
from schemas.question import CreatedQuestion


class SurveyCreated(BaseSchema):
    """
    Схема для возвращаемого опроса
    """
    id: str = Field(title="Идентификатор опроса", min_length=24, max_length=24, default=None)
    name: str = Field(title="Название опроса", min_length=5, max_length=256)
    description: Optional[str] = Field(title="Описание опроса", default=None)
    creator_id: str = Field(title="Идентификатор пользователя-создателя опроса", min_length=32, max_length=32)
    questions: list[CreatedQuestion] = Field(title="Вопросы", min_length=1)