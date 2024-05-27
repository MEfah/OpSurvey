from typing import Optional, Self, Any
from pydantic import BaseModel, Field, model_validator
from schemas.question import Question
from datetime import datetime
from models.objectId import PyObjectId
from schemas.access import AccessApi, AccessResults, AccessSurvey
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from schemas.base import BaseSchema


class SurveyCreate(BaseSchema):
    """
    Схема для создаваемого опроса
    """
    name: str = Field(title="Название опроса", min_length=5, max_length=256)
    description: Optional[str] = Field(title="Описание опроса", default=None)
    img_src: Optional[str] = Field(title="Путь к изображению опроса", default=None)
    creator_id: str = Field(title="Идентификатор пользователя-создателя опроса", min_length=32, max_length=32)
    creator_name: str = Field(title="Имя создателя опроса", min_length=5, max_length=70)
    creator_img_src: Optional[str] = Field(title="Изображение создателя опроса", default=None)
    shuffle_questions: bool = Field(title="Перемешивать вопросы", default=False)
    access_survey: AccessSurvey = Field(title="Настройки ограничений доступа к опросу", default=AccessSurvey(access_type_survey=AccessSurveyType.ALL))
    access_results: AccessResults = Field(title="Настройки ограничений доступа к результатам", default=AccessResults(access_type_results=AccessResultsType.ALL))
    access_api: Optional[AccessApi] = Field(title="Настройки ограничений доступа к API", default=AccessApi(access_type_api=AccessApiType.NONE))
    questions: list[Question] = Field(title="Вопросы", min_length=1)
    
    @model_validator(mode='after')
    def check_self(self) -> Self:
        question_ids = set()
        for question in self.questions:
            assert question.id not in question_ids, 'Идентификаторы вопросов должны быть уникальными'
            question_ids.add(question.id)
        for i in range(0, len(question_ids)):
            assert i in question_ids, 'Идентификаторы вопросов должны идти подряд'
        return self
    
    
class SurveyResponse(BaseSchema):
    """
    Схема для возвращаемого опроса
    """
    id: PyObjectId = Field(title="Идентификатор опроса", min_length=24, max_length=24, default=None)
    name: str = Field(title="Название опроса", min_length=5, max_length=256)
    description: Optional[str] = Field(title="Описание опроса", default=None)
    img_src: Optional[str] = Field(title="Путь к изображению опроса", default=None)
    creator_id: str = Field(title="Идентификатор пользователя-создателя опроса", min_length=32, max_length=32)
    creator_name: str = Field(title="Имя создателя опроса", min_length=5, max_length=70)
    creator_img_src: Optional[str] = Field(title="Изображение создателя опроса", default=None)
    creation_date: datetime = Field(title="Дата создания")
    completion_count: int = Field(title="Количество прохождений", default=0, ge=0)
    completion_time: int = Field(title="Время на прохождение в минутах", gt=0)
    shuffle_questions: bool = Field(title="Перемешивать вопросы", default=False)
    question_count: int = Field(title="Количество вопросов")
    required_count: int = Field(title="Количество обязательных вопросов")
    questions: list[Question] = Field(title="Вопросы", min_length=1)
    
    
class SurveyInfoResponse(BaseSchema):
    """
    Схема для списочного отображения опроса
    """
    id: PyObjectId = Field(title="Идентификатор опроса", min_length=24, max_length=24)
    name: str = Field(title="Название опроса", min_length=5, max_length=256)
    description: Optional[str] = Field(title="Описание опроса")
    img_src: Optional[str] = Field(title="Путь к изображению опроса")
    creator_id: str = Field(title="Идентификатор пользователя-создателя опроса", min_length=32, max_length=32)
    creator_name: str = Field(title="Имя создателя опроса", min_length=5, max_length=70)
    creator_img_src: Optional[str] = Field(title="Изображение создателя опроса")
    creation_date: datetime = Field(title="Дата создания")
    completion_count: int = Field(title="Количество прохождений", default=0, ge=0)
    completion_time: int = Field(title="Время на прохождение в минутах", gt=0)
    shuffle_questions: bool = Field(title="Перемешивать вопросы", default=False)
    question_count: int = Field(title="Количество вопросов")
    required_count: int = Field(title="Количество обязательных вопросов")

    
class SurveyInfoList(BaseSchema):
    """
    Схема списка вопросов
    """
    
    surveys: list[SurveyInfoResponse]
    
    
class AccessUpdate(BaseSchema):
    """
    Схема обновления настроек доступа
    """
    
    access_survey: Optional[AccessSurvey] = Field(title="Настройки ограничений доступа к опросу", default=None)
    access_results: Optional[AccessResults] = Field(title="Настройки ограничений доступа к результатам", default=None)
    access_api: Optional[AccessApi] = Field(title="Настройки ограничений доступа к API", default=None)
    
    # @model_validator(mode='before')
    # @classmethod
    # def check_has_no_data(cls, data: Any) -> Any:
    #     if isinstance(data, dict):
    #         assert not (('access_survey' not in data or data['access_survey'] is None) \
    #             and ('access_results' not in data or data['access_results'] is None) \
    #             and ('access_api' not in data or data['access_api'] is None) 
    #             ), 'Для обновления не указано никаких данных'
            
    #     return data
    
    
class AccessResponse(BaseSchema):
    """
    Схема ответа на обновление доступа настроек
    """
    
    access_survey: AccessSurvey = Field(title="Настройки ограничений доступа к опросу")
    access_results: AccessResults = Field(title="Настройки ограничений доступа к результатам")
    access_api: AccessApi = Field(title="Настройки ограничений доступа к API")