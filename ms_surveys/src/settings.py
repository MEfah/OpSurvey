from pydantic import BaseModel, Field, MongoDsn
import os


class Project(BaseModel):
    """
    Класс для описания проекта OpenAPI
    """
    
    title: str = "Микросервис опросов"
    description: str = "Микросервис, ответственный за создание опросов, их сохранение и загрузку"
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
    database_url: MongoDsn = Field(
        default=f"mongodb://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@db_surveys/{os.getenv("MONGO_DB")}?retryWrites=true&w=majority"
        )
    project: Project = Project()
    jwt: JWTSettings = JWTSettings()
    rabbit: RabbitSettings = RabbitSettings()


settings = Settings()