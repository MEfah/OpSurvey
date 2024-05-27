from typing import Optional, Any
from schemas.base import BaseSchema

from pydantic import BaseModel, Field, model_validator


class UserResponse(BaseSchema):
    """
    Схема для возвращаемых данных о пользователе
    """
    id: str = Field(title="Идентификатор пользователя", default=None, primary_key=True, min_length=32, max_length=32)
    name: str = Field(title="Имя пользователя", min_length=5, max_length=70)
    description: Optional[str] = Field(title="Доп. информация о пользователе", default=None)
    img_src: Optional[str] = Field(title="Путь к изображению аккаунта", default=None)
    
    
class UserUpdate(BaseSchema):
    """
    Схема для обновления информации об аккаунте пользователя
    """
    
    name: Optional[str] = Field(title="Имя пользователя", default=None, min_length=5, max_length=70)
    description: Optional[str] = Field(title="Доп. информация о пользователе", default=None)
    img_src: Optional[str] = Field(title="Путь к изображению аккаунта", default=None)
    
    # @model_validator(mode='before')
    # @classmethod
    # def check_has_no_data(cls, data: Any) -> Any:
    #     if isinstance(data, dict):
    #         assert not (
    #             ('name' not in data or data['name'] is None) 
    #                 and ('description' not in data or data['description'] is None) 
    #                 and ('img_src' not in data or data['img_src'] is None)
    #         ), 'Не указана информация для обновления пользователя'
    #     return data