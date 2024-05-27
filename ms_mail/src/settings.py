from pydantic import BaseModel, Field
import os


class Project(BaseModel):
    """
    Класс для описания проекта OpenAPI
    """
    
    title: str = "Микросервис почты"
    description: str = "Микросервис, ответственный за отправление электронной почты"
    version: str = Field(default="0.1.0")


class JWTSettings(BaseModel):
    """
    Класс для описания параметров JWT
    """
    
    access_secret: str = os.getenv("JWT_ACCESS_SECRET")


class EmailSettings(BaseModel):
    """Класс с почтой и паролем"""
    address: str = os.getenv('EMAIL_ADDRESS')
    password: str = os.getenv('EMAIL_PASSWORD')


class Settings(BaseModel):
    """
    Настройки микросервиса
    """
    
    debug: bool = Field(default=True)
    project: Project = Project()
    jwt: JWTSettings = JWTSettings()
    email: EmailSettings = EmailSettings()
    

settings = Settings()