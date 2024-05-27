from typing import Optional, Self
from pydantic import BaseModel, Field, model_validator
from models.option import QuestionOption
from models.enums.question import QuestionType
from schemas.base import BaseSchema


class Question(BaseSchema):
    """
    Модель вопроса
    """
    
    id: int = Field(title="Порядковый номер вопроса", ge=0)
    name: str = Field(title="Заголовок вопроса", min_length=5, max_length=256)
    description: Optional[str] = Field(title="Описание вопроса", default=None)
    question_type: QuestionType = Field(title="Тип вопроса")
    required: bool = Field(title="Обязательный", default=False)
    shuffle_options: bool = Field(title="Перемешивать варианты", default=False)
    options: Optional[list[QuestionOption]] = Field(title="Список вариантов", default=None, min_length=2)
    
    @model_validator(mode='after')
    def check_self(self) -> Self:
        if self.question_type not in [QuestionType.DROP_DOWN, QuestionType.MULTI_SELECT, QuestionType.MULTI_SELECT_OTHER, 
                                      QuestionType.SINGLE_SELECT, QuestionType.SINGLE_SELECT_OTHER]:
            return self
        assert self.options is not None, 'Для выбранного типа вопроса должны быть указаны варианты ответа'
        option_ids = set()
        for option in self.options:
            assert option.id not in option_ids, 'Идентификаторы вариантов ответов должны быть уникальными'
            option_ids.add(option.id)
        for i in range(0, len(option_ids)):
            assert i in option_ids, 'Идентификаторы вариантов ответов должны идти подряд'
        return self
    
    
class UnfinishedQuestion(BaseSchema):
    """
    Модель незавершенного опроса
    """
    
    id: int = Field(title="Порядковый номер вопроса", ge=0)
    name: Optional[str] = Field(title="Заголовок вопроса", default=None)
    description: Optional[str] = Field(title="Описание вопроса", default=None)
    question_type: QuestionType = Field(title="Тип вопроса")
    required: bool = Field(title="Обязательный", default=False)
    shuffle_options: bool = Field(title="Перемешивать варианты", default=False)
    options: Optional[list[QuestionOption]] = Field(title="Список вариантов", default=None)