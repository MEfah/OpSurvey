from typing import Optional, Self
from pydantic import BaseModel, ConfigDict, Field, model_validator, ValidationError
from datetime import datetime
from models.access import AccessApi, AccessResults, AccessSurvey
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from models.objectId import PyObjectId


class Survey(BaseModel):
    """
    Модель опроса
    """
    
    id: Optional[PyObjectId] = Field(title="Идентификатор опроса", alias='_id', min_length=24, max_length=24, default=None)
    creator_id: str = Field(title="Идентификатор пользователя-создателя опроса", min_length=32, max_length=32)
    access_survey: AccessSurvey = Field(title="Настройки ограничений доступа к опросу", default=AccessSurvey(access_type_survey=AccessSurveyType.ALL))
    access_results: AccessResults = Field(title="Настройки ограничений доступа к результатам", default=AccessResults(access_type_results=AccessResultsType.ALL))
    access_api: AccessApi = Field(title="Настройки ограничений доступа к API", default=AccessApi(access_type_api=AccessApiType.NONE))
    question_types: list[int] = Field(title="Типы вопросов", min_length=1)

    model_config = ConfigDict(
        populate_by_name=True
    )