from typing import Optional
from schemas.validators import is_email
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from schemas.users import UserResponse
from schemas.base import BaseSchema


class SignUpInfo(BaseSchema):
    """
    Схема для данных, вводимых при создании аккаунта
    """
    
    name: str = Field(default=None, min_length=5, max_length=70)
    email: str = Field(default=None, min_length=5)
    password: str = Field(default=None, min_length=5)
    
    @field_validator('email')
    @classmethod
    def check_is_email(cls, v: str, info: ValidationInfo) -> str:
        str_is_email = is_email(v)
        assert str_is_email, f'{info.field_name} не является корректным email\'ом'
        return v
    
    
class SignInInfo(BaseSchema):
    """
    Схема для данных, вводимых при входе в аккаунт
    """
    
    email: str = Field(default=None, min_length=5)
    password: str = Field(default=None, min_length=5)
    
    @field_validator('email')
    @classmethod
    def check_is_email(cls, v: str, info: ValidationInfo) -> str:
        str_is_email = is_email(v)
        assert str_is_email, f'{info.field_name} не является корректным email\'ом'
        return v
    
    
class AuthResponse(BaseSchema):
    """
    Схема для данных, возвращаемых при авторизации
    """
    
    user: UserResponse = Field()
    access_token: str = Field()
    refresh_token: str = Field()
    
    
class RefreshResponse(BaseSchema):
    """
    Схема для данных, возвращаемых при обновлении токена
    """
    access_token: str = Field()
    refresh_token: str = Field()
    