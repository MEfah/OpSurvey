from typing import Optional
from sqlmodel import SQLModel, Field


class Survey(SQLModel, table=True):
    """
    Модель опроса
    """
    # Для экономии места вместо guid добавляем отдельный целочисленный идентификаторр
    doc_id: Optional[int] = Field(title="Идентификатор опроса как документа", primary_key=True, default=None)
    id: str = Field(title="Идентификатор опроса", min_length=24, max_length=24, default=None, index=True, unique=True)
    creator_id: str = Field(title="Идентификатор пользователя-создателя опроса", min_length=32, max_length=32)
    access_type: int = Field(title="Тип доступа к опросу")