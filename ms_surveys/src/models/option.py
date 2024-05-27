from typing import Optional
from pydantic import BaseModel, Field


class QuestionOption(BaseModel):
    """
    Модель варианта ответа на вопрос
    """
    
    id: int = Field(title="Порядковый номер варианта", ge=0)
    name: str = Field(title="Текст варианта", min_length=1)