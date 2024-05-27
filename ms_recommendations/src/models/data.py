from sqlmodel import SQLModel, Field


class Data(SQLModel, table=True):
    """
    Модель данных для составления рекомендаций
    """
    # Для экономии места вместо guid добавляем отдельный целочисленный идентификаторр
    doc_id: int = Field(title="Идентификатор опроса как документа", primary_key=True)
    word_id: int = Field(title="Идентификатор слова", primary_key=True)
    count: int = Field(title="Количество вхождений слова в документ")