from typing import Optional, Self
from pydantic import BaseModel, ConfigDict, Field, model_validator, ValidationError
from datetime import datetime
from models.access import AccessApi, AccessResults, AccessSurvey
from models.question import Question, UnfinishedQuestion
from models.enums.access import AccessApiType, AccessResultsType, AccessSurveyType
from models.objectId import PyObjectId


class Survey(BaseModel):
    """
    Модель опроса
    """
    
    id: Optional[PyObjectId] = Field(title="Идентификатор опроса", alias='_id', min_length=24, max_length=24, default=None)
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
    access_survey: AccessSurvey = Field(title="Настройки ограничений доступа к опросу", default=AccessSurvey(access_type_survey=AccessSurveyType.ALL))
    access_results: AccessResults = Field(title="Настройки ограничений доступа к результатам", default=AccessResults(access_type_results=AccessResultsType.ALL))
    access_api: AccessApi = Field(title="Настройки ограничений доступа к API", default=AccessApi(access_type_api=AccessApiType.NONE))
    question_count: int = Field(title="Количество вопросов")
    required_count: int = Field(title="Количество обязательных вопросов")
    questions: list[Question] = Field(title="Вопросы", min_length=1)
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    @model_validator(mode='after')
    def check_self(self) -> Self:
        question_ids = set()
        for question in self.questions:
            assert question.id not in question_ids, 'Идентификаторы вопросов должны быть уникальными'
            question_ids.add(question.id)
        for i in range(0, len(question_ids)):
            assert i in question_ids, 'Идентификаторы вопросов должны идти подряд'
        return self


class UnfinishedSurvey(BaseModel):
    """
    Модель незаконченного опроса
    """
    id: Optional[PyObjectId] = Field(title="Идентификатор опроса", alias='_id', min_length=24, max_length=24, default=None)
    name: str = Field(title="Название опроса", min_length=5, max_length=256)
    description: Optional[str] = Field(title="Описание опроса", default=None)
    img_src: Optional[str] = Field(title="Путь к изображению опроса", default=None)
    creator_id: str = Field(title="Идентификатор пользователя-создателя опроса", min_length=32, max_length=32)
    updated_date: datetime = Field(title="Дата изменения")
    shuffle_questions: bool = Field(title="Перемешивать вопросы", default=False)
    questions: list[UnfinishedQuestion] = Field(title="Вопросы", min_length=1)
    model_config = ConfigDict(
        populate_by_name=True
    )