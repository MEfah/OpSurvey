from typing import Optional, Self
from pydantic import BaseModel, Field, model_validator
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from schemas.base import BaseSchema


class AccessSurvey(BaseSchema):
    """
    Настройки ограничений доступа к опросу
    """
    
    access_type_survey: AccessSurveyType = Field(title="Идентификатор типа ограничения доступа к опросу")
    access_list: Optional[list[str]] = Field(title="Список пользователей, кому позволен доступ", default=None)
    access_keys: Optional[list[str]] = Field(title="Список ключей доступа", default=None)
    
    @model_validator(mode='after')
    def check_self(self) -> Self:
        """Проверить, что для списочных типов вопросов указаны списки
        """
        if self.access_type_survey == AccessSurveyType.ONLY_LIST:
            assert self.access_list is not None and len(self.access_list) > 0, \
                'При ограничении доступа по списку необходимо указать список пользователей'
                
            for id in self.access_list:
                assert len(id) == 32, 'Некорректный формат элементов списка пользователей'
                
        if self.access_type_survey == AccessSurveyType.ONLY_KEYS:
            assert self.access_keys is not None and len(self.access_keys) > 0, \
                'При ограничении доступа по ключам необходимо указать список ключей'
                
        if self.access_type_survey == AccessSurveyType.ONLY_LIST_AND_KEYS:
            assert self.access_list is not None and len(self.access_list) > 0 and self.access_keys is not None and len(self.access_keys) > 1, \
                'При ограничении доступа по ключам и списку необходимо указать списки пользователей и ключей'
            
        return self


class AccessResults(BaseSchema):
    """
    Настройки ограничений доступа к результатам
    """

    access_type_results: AccessResultsType = Field(title="Идентификатор типа ограничения доступа к результатам опроса")
    access_list: Optional[list[str]] = Field(title="Список пользователей, кому позволен доступ", default=None)
    
    @model_validator(mode='after')
    def check_self(self) -> Self:
        if self.access_type_results in [AccessResultsType.ONLY_LIST]:
            assert self.access_list is not None and len(self.access_list) > 0, \
                'При ограничении доступа по списку, необходимо указать список пользователей'
        return self
    
    
class AccessApi(BaseSchema):
    """
    Настройки ограничений доступа к API
    """

    access_type_api: AccessApiType = Field(title="Идентификатор типа ограничения доступа к API")
    access_list: Optional[list[str]] = Field(title="Список пользователей, кому позволен доступ", default=None)
    
    @model_validator(mode='after')
    def check_self(self) -> Self:
        if self.access_type_api in [AccessApiType.ONLY_LIST]:
            assert self.access_list is not None and len(self.access_list) > 0, \
                'При ограничении доступа по списку, необходимо указать список пользователей'
        return self