from pydantic import Field
from schemas.base import BaseSchema


class EmailInfo(BaseSchema):
    text: str = Field(title='Текст сообщения')
    to: list[str] = Field(title='Адреса электронных почт получателей')