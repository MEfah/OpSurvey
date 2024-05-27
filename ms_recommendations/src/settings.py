from pydantic import BaseModel, Field, PostgresDsn
import os


class Project(BaseModel):
    """
    Класс для описания проекта OpenAPI
    """
    
    title: str = "Микросервис рекомендаций"
    description: str = "Микросервис, ответственный за формирование рекомендаций"
    version: str = Field(default="0.1.0")


class JWTSettings(BaseModel):
    """
    Класс для описания параметров JWT
    """
    
    access_secret: str = os.getenv("JWT_ACCESS_SECRET")


class RabbitSettings(BaseModel):
    """
    Класс для описания параметров Rabbit
    """
    
    _user = os.getenv("RABBITMQ_USER")
    _pass = os.getenv("RABBITMQ_PASSWORD")
    connection_string: str = f"amqp://{_user}:{_pass}@rabbit/"


class Settings(BaseModel):
    """
    Настройки микросервиса
    """
    
    debug: bool = Field(default=True)
    database_url: PostgresDsn = Field(
        default=f"postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@db_recommendations/{os.getenv("POSTGRES_DB")}"
        )
    project: Project = Project()
    jwt: JWTSettings = JWTSettings()
    cookie_id_ttl_days: int = 365
    rabbit: RabbitSettings = RabbitSettings()


settings = Settings()