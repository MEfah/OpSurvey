from pydantic import Field
from schemas.base import BaseSchema


class AnswerCreated(BaseSchema):
    """
    Схема информации о созданном опросе
    """
    
    user_id: str = Field(title="Идентификатор пользователя", min_length=32, max_length=32, default=None)
    survey_id: str = Field(title="Идентификатор опроса", min_length=24, max_length=24)

