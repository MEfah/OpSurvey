from typing import Optional, Self, Any, Annotated
from pydantic import BaseModel, Field, model_validator
from models.question import Question
from datetime import datetime
from models.objectId import PyObjectId
from models.access import AccessApi, AccessResults, AccessSurvey
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from schemas.base import BaseSchema
from schemas.enums.sort import SortType
from schemas.filter import FilterParam


class SearchParams(BaseSchema):
    """
    Схема поискового запроса
    """
    filter_params: list[FilterParam] | None = Field(default=None, min_length=1)
    search_text: str | None = Field(default=None)
    sort_type:SortType | None = Field(default=None)
    sort_ascending: bool | None = Field(default=None)