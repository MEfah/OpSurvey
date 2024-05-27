import pytest
import pytest_asyncio
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.recommendations import RecommendationsRepository

from models.survey import Survey
from models.data import Data
from models.completion import Completion


@pytest.mark.usefixtures("session")
class TestRecommendationsRepository:
    """
    Тестирование репозитория рекомендаций.
    """

    @pytest_asyncio.fixture
    async def repository(self, session):
        """Фикстура тестируемого репозитория"""

        yield RecommendationsRepository(session)


    @pytest.mark.asyncio
    async def test_insert_bow(self, repository: RecommendationsRepository):
        """
        Проверить добавление bag of words
        Успешный сценарий
        """
        initial_bow = [
            (0, 0, 1),
            (0, 1, 1),
            (1, 1, 1),
            (2, 0, 2),
            (2, 1, 1)
        ]
        
        await repository.insert_bow(initial_bow)
        
        res = await repository.get_bow()

        assert sorted(initial_bow) == sorted(res)


    @pytest.mark.asyncio
    async def test_insert_bow_dublicate(self, repository: RecommendationsRepository):
        """
        Проверить добавление bag of words
        Ошибка: нарушение уникальности в добавляемом списке
        """
        initial_bow = [
            (0, 0, 1),
            (0, 0, 1),
            (0, 1, 1),
            (1, 1, 1),
            (2, 0, 2),
            (2, 1, 1)
        ]
        
        with pytest.raises(IntegrityError):
            await repository.insert_bow(initial_bow)


    @pytest.mark.asyncio
    async def test_insert_bow_dublicate2(self, repository: RecommendationsRepository):
        """
        Проверить добавление bag of words
        Ошибка: нарушение уникальности - в бд уже есть добавляемая запись
        """
        initial_bow = [
            (0, 0, 1),
            (0, 1, 1),
            (1, 1, 1),
            (2, 0, 2),
            (2, 1, 1)
        ]
        await repository.insert_bow(initial_bow)
        
        with pytest.raises(IntegrityError):
            await repository.insert_bow([(1, 1, 1), (3, 0, 1)])


    @pytest.mark.asyncio
    async def test_add_survey(self, session: AsyncSession, repository: RecommendationsRepository):
        """
        Проверить добавление опроса
        Успешный сценарий
        """
        initial_survey = Survey(id='123456781234567812345678', creator_id='12345678123456781234567812345678', access_type=0)
        res = await repository.add_survey(initial_survey)

        get: Survey = (await session.execute(select(Survey).where(Survey.id==initial_survey.id))).first()[0]

        assert get.id == initial_survey.id
        assert get.creator_id == initial_survey.creator_id
        assert get.access_type == initial_survey.access_type
        assert get.doc_id == res


    @pytest.mark.asyncio
    async def test_add_survey_duplicate(self, repository: RecommendationsRepository):
        """
        Проверить добавление опроса
        Нарушение уникальности
        """
        initial_survey = Survey(id='123456781234567812345678', creator_id='12345678123456781234567812345678', access_type=0)
        res = await repository.add_survey(initial_survey)
        
        with pytest.raises(IntegrityError):
            await repository.add_survey(initial_survey)
            
    
    @pytest.mark.asyncio
    async def test_add_survey_duplicate(self, repository: RecommendationsRepository):
        """
        Проверить добавление опроса
        Нарушение уникальности
        """
        initial_survey = Survey(id='123456781234567812345678', creator_id='12345678123456781234567812345678', access_type=0)
        res = await repository.add_survey(initial_survey)
        
        with pytest.raises(IntegrityError):
            await repository.add_survey(initial_survey)
            
            
    @pytest.mark.asyncio
    async def test_get_survey_doc_id(self, repository: RecommendationsRepository):
        """Проверить получение номера документа опроса"""
        initial_survey = Survey(id='123456781234567812345678', creator_id='12345678123456781234567812345678', access_type=0)
        insert_res = await repository.add_survey(initial_survey)
        
        get = await repository.get_survey_doc_id(initial_survey.id)

        assert get == insert_res
        
        
    @pytest.mark.asyncio
    async def test_insert_and_get_words_new(self, repository: RecommendationsRepository):
        """Проверить добавление новых слов в базу данных"""
        
        res = await repository.insert_and_get_words(['word1', 'word2', 'word3'])
        
        assert 'word1' in res
        assert 'word2' in res
        assert 'word3' in res
        assert res['word1'] != res['word2']
        assert res['word3'] != res['word2']
        assert res['word1'] != res['word3']
        
        
    @pytest.mark.asyncio
    async def test_insert_and_get_words_old(self, repository: RecommendationsRepository):
        """Проверить добавление слов в базу данных, включая уже существующие"""
        
        res = await repository.insert_and_get_words(['word1', 'word2', 'word3'])
        res2 = await repository.insert_and_get_words(['word2', 'word3', 'word4'])
        
        assert res['word2'] == res2['word2']
        assert res['word3'] == res2['word3']
        assert res['word1'] < res2['word4']
    
    
    @pytest.mark.asyncio
    async def test_update_survey_access(self, session: AsyncSession, repository: RecommendationsRepository):
        """Проверить обновление настроек доступа опроса"""
        initial_survey = Survey(id='123456781234567812345678', creator_id='12345678123456781234567812345678', access_type=0)
        new_access_type = 2
        await repository.add_survey(initial_survey)
        
        await repository.update_survey_access(initial_survey.id, new_access=new_access_type)
        
        res = (await session.execute(select(Survey.access_type).where(Survey.id == initial_survey.id))).first()[0]
        
        assert res == new_access_type
        
    
    @pytest.mark.asyncio
    async def test_add_completion(self, session: AsyncSession, repository: RecommendationsRepository):
        """Проверить добавление записи о прохождении опроса"""
        survey = Survey(id='123456781234567812345678', creator_id='12345678123456781234567812345678', access_type=0)
        doc_id = await repository.add_survey(survey)
        
        await repository.add_completion(survey_id=survey.id, user_id=survey.creator_id)
        
        res = (await session.execute(select(Completion.doc_id, Completion.user_id).
                                    where(Completion.user_id == survey.creator_id))).first()
        assert res[0] == doc_id
        assert res[1] == survey.creator_id
        
        
    @pytest.mark.asyncio
    async def test_get_user_surveys(self, repository: RecommendationsRepository):
        """Проверить добавление записи о прохождении опроса"""
        survey = Survey(id='123456781234567812345678', creator_id='12345678123456781234567812345678', access_type=0)
        doc_id = await repository.add_survey(survey)
        words = await repository.insert_and_get_words(['word1', 'word2', 'word3'])
        bow = [
          (doc_id, words['word1'], 4),
          (doc_id, words['word2'], 5),
          (doc_id, words['word3'], 6)
        ]
        await repository.insert_bow(bow)
        await repository.add_completion(survey_id=survey.id, user_id=survey.creator_id)
        
        res = await repository.get_user_surveys(survey.creator_id)
        assert sorted(bow) == sorted(res)