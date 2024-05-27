from pydantic import Field
from schemas.base import BaseSchema


class AuthInfo(BaseSchema):
    """
    Класс для хранения информации о пользователе
    """
    
    authorized: bool = Field(title="Авторизован ли пользователь", default=False)
    user_id: str = Field(title="Идентификатор пользователя")