from typing import Optional
from pydantic import BaseModel, Field
from models.enums.access import AccessSurveyType
from schemas.base import BaseSchema


class AccessSurvey(BaseModel):
    """
    Настройки ограничений доступа к опросу
    """
    
    access_type_survey: AccessSurveyType = Field(title="Идентификатор типа ограничения доступа к опросу")
    access_list: Optional[list[str]] = Field(title="Список пользователей, кому позволен доступ", default=None)
    access_keys: Optional[list[str]] = Field(title="Список ключей доступа", default=None)
    
    
class AccessUpdated(BaseSchema):
    """
    Схема информации об обновлении прав доступа к опросу
    """
    
    access_survey: Optional[AccessSurvey] = Field(title="Настройки ограничений доступа к опросу", default=None)


class AccessUpdatedInfo(BaseSchema):
    """Схема сообщения об изменения прав доступа к опросу"""
    id: str = Field(title="Идентификатор опроса", min_length=24, max_length=24)
    access_updated: AccessUpdated = Field(title="Изменения прав доступа")
