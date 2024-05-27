from typing import Optional, Self
from pydantic import BaseModel, ConfigDict, Field, model_validator, ValidationError
from datetime import datetime
from models.access import AccessApi, AccessResults, AccessSurvey
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from models.objectId import PyObjectId
from schemas.base import BaseSchema


class AccessUpdated(BaseSchema):
    """
    Схема информации об обновлении прав доступа к опросу
    """
    
    access_survey: Optional[AccessSurvey] = Field(title="Настройки ограничений доступа к опросу", default=None)
    access_results: Optional[AccessResults] = Field(title="Настройки ограничений доступа к результатам", default=None)
    access_api: Optional[AccessApi] = Field(title="Настройки ограничений доступа к API", default=None)


class AccessUpdatedInfo(BaseSchema):
    """Схема сообщения об изменения прав доступа к опросу"""
    id: str = Field(title="Идентификатор опроса", min_length=24, max_length=24)
    access_updated: AccessUpdated = Field(title="Изменения прав доступа")
