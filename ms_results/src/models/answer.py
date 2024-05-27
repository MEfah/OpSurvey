from typing import Optional, Self
from pydantic import BaseModel, ConfigDict, Field, model_validator, ValidationError
from datetime import datetime
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from models.objectId import PyObjectId

    
class QuestionAnswer(BaseModel):
    """Модель ответа на вопрос"""
    id: int = Field(title="Номер вопроса")
    value: str | int | float | datetime | None = Field(title="Ответ на вопрос", default=None)
    options: list[int] | None = Field(title="Выбранные варианты ответа", default=None)


class SurveyAnswer(BaseModel):
    """
    Модель ответа на опрос
    """
    id: Optional[PyObjectId] = Field(title="Идентификатор ответа", alias='_id', default=None)
    is_finished: bool = Field(title="Ответ закончен", default=False)
    survey_id: str = Field(title="Идентификатор опроса", min_length=24, max_length=24)
    user_id: str = Field(title="Идентификатор пользователя", min_length=32, max_length=32)
    question_answers: list[QuestionAnswer] = Field(title='Ответы на вопросы')