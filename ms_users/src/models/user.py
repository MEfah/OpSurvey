from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    """
    Модель пользователя
    """
    
    id: str = Field(title="Идентификатор пользователя", default=None, primary_key=True, min_length=32, max_length=32)
    email: str = Field(title="Email пользователя", default=None, unique=True, min_length=5)
    password: str = Field(title="Хэш пароля пользователя", default=None)
    name: str = Field(title="Имя пользователя", default=None, min_length=5, max_length=70, unique=True)
    description: Optional[str] = Field(title="Доп. информация о пользователе", default=None)
    img_src: Optional[str] = Field(title="Путь к изображению аккаунта", default=None)