from typing import Optional, Self, Any
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from models.objectId import PyObjectId
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from schemas.base import BaseSchema

    
class QuestionAnswer(BaseSchema):
    """Модель ответа на вопрос"""
    id: int = Field(title="Номер вопроса")
    value: str | int | float | datetime | None = Field(title="Ответ на вопрос", default=None)
    options: list[int] | None = Field(title="Выбранные варианты ответа", default=None)
    
    
class SurveyAnswerResponse(BaseSchema):
    """
    Схема ответа на опрос
    """
    survey_id: str = Field(title="Идентификатор опроса", min_length=24, max_length=24)
    user_id: str = Field(title="Идентификатор пользователя", min_length=32, max_length=32)
    is_finished: bool = Field(title="Ответ завершен", default=False)
    question_answers: list[QuestionAnswer] = Field(title='Ответы на вопросы', min_length=1)
    

class SurveyAnswerCreate(BaseSchema):
    is_finished: bool = Field(title="Ответ завершен", default=False)
    question_answers: list[QuestionAnswer] = Field(title='Ответы на вопросы', min_length=1)
    
class SurveyAnswerList(BaseSchema):
    """Схема списка ответов на опрос"""
    answers: list[SurveyAnswerResponse] = Field(title='Ответы на опрос')