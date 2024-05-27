from typing import Optional, Any
from pydantic import BaseModel, Field, model_validator
from models.question import Question
from datetime import datetime
from models.objectId import PyObjectId
from models.access import AccessApi, AccessResults, AccessSurvey
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from schemas.enums.filter import FilterParameterType
from datetime import datetime, time
from schemas.base import BaseSchema

        
class FilterRange(BaseSchema):
    """Схема промежутка для передачи информации о фильтрации
    """
    range_from: int | float | datetime | time | None = Field(title="Начало промежутка", alias='from', default=None)
    range_to: int | float | datetime | time | None = Field(title="Конец промежутка", alias='to', default=None)
    
    
    
class FilterParam(BaseSchema):
    """
    Схема для параметров фильтрации
    """
    
    parameter_type: FilterParameterType = Field(title="Тип параметра фильтрации")
    value: FilterRange | None = Field(title="Значение для фильтрации", default=None)
    
    
class FilterParamList(BaseSchema):
    """
    Схема списка параметров фильтрации
    """
    filter_params: list[FilterParam] = Field(title='Список параметров фильтрации', min_length=1)