from typing import List, Tuple
from models.data import Data
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, insert, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlmodel.sql.expression import SelectOfScalar
from models.survey import Survey
from models.enums.access import AccessSurveyType
from models.completion import Completion
from models.data import Data
from models.dictionary import Word
import uuid


class RecommendationsRepository():
    """
    Репозиторий для пользователей
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализация репозитория
        """
        self.session = session
        print(session)
        
    
    async def get_survey_doc_id(self, survey_id: str) -> None:
        stmt = select(Survey.doc_id).where(Survey.id == survey_id)
        doc_id = (await self.session.execute(stmt)).first()[0]
        return doc_id
    
    
    async def insert_and_get_words(self, words: list[str]) -> dict:
        """Получить идентификаторы слов из бд"""
        stmt = pg_insert(Word).values([{Word.text: value} for value in words]).on_conflict_do_nothing()
        await self.session.execute(stmt)
        stmt_select = select(Word.text, Word.word_id).where(Word.text.in_(words))
        result_dict = await (self.session.execute(stmt_select))
        return {word: ind for word, ind in result_dict}
    
    
    async def get_bow(self) -> List[Tuple[int, int, int]]:
        """Получить bag of words"""
        return (await self.session.execute(select(Data.doc_id, Data.word_id, Data.count))).all()
    
        
    async def insert_bow(self, bow: List[Tuple[int, int, int]]) -> None:
        """Вставить bag of words в бд"""
        data_objects = [Data(doc_id=doc_id, word_id=word_id, count=count) for doc_id, word_id, count in bow]
        await self.session.execute(insert(Data), data_objects)
        await self.session.commit()
        
    
    async def add_survey(self, survey: Survey) -> int:
        """Добавить опрос в базу данных и получить идентификатор опроса как документа

        Args:
            survey (Survey): новый опрос

        Returns:
            int: идентификатор опроса, как документа
        """
        cursor = await self.session.execute(insert(Survey).returning(Survey.doc_id), [survey])
        doc_id = cursor.fetchone()
        await self.session.commit()
        return doc_id[0]
        
        
    async def update_survey_access(self, survey_id: str, new_access: AccessSurveyType):
        """Обновить доступ к опросу"""
        statement = (
            update(Survey)
            .where(Survey.id == survey_id)
            .values(access_type = new_access)
        )
        await self.session.execute(statement)
        await self.session.commit()
    
    
    async def add_completion(self, user_id: str, survey_id: str):
        """Добавить запись о прохождении пользователем опроса"""
        stmt = select(Survey.doc_id).where(Survey.id == survey_id)
        doc_id = (await self.session.execute(stmt)).first()
        completion = Completion(user_id=user_id, doc_id=doc_id[0])
        self.session.add(completion)
        await self.session.commit()


    async def get_user_surveys(self, user_id: str) -> List[Tuple[int, int, int]]:
        """Получить bag of words опросов пользователя"""
        stmt = select(Data.doc_id, Data.word_id, Data.count).join(Completion, Completion.doc_id == Data.doc_id).where(Completion.user_id == user_id)
        res = (await self.session.execute(stmt)).all()
        return res