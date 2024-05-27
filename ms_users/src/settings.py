from pydantic import BaseModel, Field, PostgresDsn
import os


class Project(BaseModel):
    """
    Класс для описания проекта OpenAPI
    """
    
    title: str = "Микросервис пользователей"
    description: str = "Микросервис, ответственный за создание и изменение учетных записей, аутентификацию и авторизацию"
    version: str = Field(default="0.1.0")


class JWTSettings(BaseModel):
    """
    Класс для описания параметров JWT
    """
    
    access_secret: str = os.getenv("JWT_ACCESS_SECRET")
    access_ttl_min: int = int(os.getenv("JWT_ACCESS_TTL"))
    refresh_secret: str = os.getenv("JWT_REFRESH_SECRET")
    refresh_ttl_days: int = int(os.getenv("JWT_REFRESH_TTL"))


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
        default=f"postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@db_users/{os.getenv("POSTGRES_DB")}"
        )
    project: Project = Project()
    jwt: JWTSettings = JWTSettings()
    cookie_id_ttl_days: int = 365
    rabbit: RabbitSettings = RabbitSettings()


settings = Settings()