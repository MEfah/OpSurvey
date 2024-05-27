from sqlmodel import SQLModel, Field, Column, DateTime
from datetime import datetime


class Completion(SQLModel, table=True):
    """
    Модель данных с историей прохождений
    """
    # Для экономии места вместо guid добавляем отдельный целочисленный идентификаторр
    user_id: str = Field(title="Идентификатор пользователя", primary_key=True)
    doc_id: int = Field(title="Идентификатор пройденного опроса", primary_key=True)
    dt: datetime = Field(title="Дата прохождения", sa_column=Column(DateTime, default=datetime.utcnow, nullable=False,))