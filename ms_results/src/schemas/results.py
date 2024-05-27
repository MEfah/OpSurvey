from typing import Optional, Self, Any
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from models.objectId import PyObjectId
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from schemas.base import BaseSchema


class OptionsResult(BaseSchema):
    id: int = Field(title="Номер варианта ответа")
    count: int = Field(title="Количество раз, которое вариант был выбран")
    
    
class OptionsResults(BaseSchema):
    options: list[OptionsResult] = Field(title="Информация о выборе вариантов ответов")
    
    
class ValueInterval(BaseSchema):
    from_value: int | float | datetime = Field(title="Начало интервала", alias="from")
    count: int = Field(title="Количество значений в интервале")
    
    
class ValueResults(BaseSchema):
    min: int | float | datetime = Field(title="Минимальное значение")
    max: int | float | datetime = Field(title="Максимальное значение")
    mean: int | float | datetime = Field(title="Среднее значение")
    intervals: list[ValueInterval] = Field("Интервалы для гистограммы")
    
    
class QuestionResults(BaseSchema):
    id: int = Field(title="Номер вопроса")
    answers_count: int = Field("Количество ответов")
    result: OptionsResults | ValueResults | None = Field(title="Агрегированные результаты ответов на вопрос")
    
    
class SurveyResults(BaseSchema):
    survey_id: str = Field(title="Идентификатор опроса", min_length=24, max_length=24, default=None)
    results: list[QuestionResults] = Field(title="Агрегированная информация об ответах на вопросы")