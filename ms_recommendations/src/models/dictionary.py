from sqlmodel import SQLModel, Field


class Word(SQLModel, table=True):
    """
    Модель данных для составления рекомендаций
    """
    word_id: int = Field(title="Идентификатор слова", primary_key=True)
    text: str = Field(title="Текст слова", unique=True, index=True)