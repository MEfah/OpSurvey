from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from models.objectId import PyObjectId
from models.access import AccessApi, AccessResults, AccessSurvey
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from schemas.question import UnfinishedQuestion
from schemas.base import BaseSchema


class UnfinishedCreate(BaseSchema):
    """
    Схема для создаваемого незаконченного опроса
    """
    name: Optional[str] = Field(title="Название опроса", default=None)
    description: Optional[str] = Field(title="Описание опроса", default=None)
    img_src: Optional[str] = Field(title="Путь к изображению опроса", default=None)
    creator_id: Optional[str] = Field(title="Идентификатор пользователя-создателя опроса", min_length=32, max_length=32, default=None)
    shuffle_questions: bool = Field(title="Перемешивать вопросы", default=False)
    questions: Optional[list[UnfinishedQuestion]] = Field(title="Вопросы", min_length=1, default=None)
    
    
class UnfinishedResponse(BaseSchema):
    """
    Схема для возвращаемого незаконченного опроса
    """
    id: PyObjectId = Field(title="Идентификатор опроса", min_length=24, max_length=24)
    name: Optional[str] = Field(title="Название опроса", default=None)
    description: Optional[str] = Field(title="Описание опроса", default=None)
    img_src: Optional[str] = Field(title="Путь к изображению опроса", default=None)
    creator_id: str = Field(title="Идентификатор пользователя-создателя опроса", min_length=32, max_length=32)
    shuffle_questions: bool = Field(title="Перемешивать вопросы", default=False)
    updated_date: datetime = Field(title="Дата изменения")
    questions: Optional[list[UnfinishedQuestion]] = Field(title="Вопросы", min_length=1, default=None)
    
    
class UnfinishedInfoResponse(BaseSchema):
    """
    Схема для списочного отображения незаконченного опроса
    """
    id: PyObjectId = Field(title="Идентификатор опроса", min_length=24, max_length=24)
    name: Optional[str] = Field(title="Название опроса", default=None)
    description: Optional[str] = Field(title="Описание опроса", default=None)
    img_src: Optional[str] = Field(title="Путь к изображению опроса", default=None)
    creator_id: str = Field(title="Идентификатор пользователя-создателя опроса", min_length=32, max_length=32)
    updated_date: datetime = Field(title="Дата изменения")
    
    
class UnfinishedInfoList(BaseSchema):
    """
    Схема списка вопросов
    """
    
    surveys: list[UnfinishedInfoResponse]