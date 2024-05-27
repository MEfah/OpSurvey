import pytest
import pytest_asyncio
from pytest_mock import MockerFixture
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.recommendations import RecommendationsRepository

from models.survey import Survey
from models.data import Data
from models.completion import Completion

from services.tf_idf import TfIdfMatrix


@pytest.mark.usefixtures("session")
class TestRecommendationsRepository:
    """
    Тестирование репозитория для списка любимых мест.
    """

    @pytest_asyncio.fixture
    async def repository(self, session):
        """Фикстура репозитория для тестирования"""

        yield RecommendationsRepository(session)


    @pytest_asyncio.fixture
    async def mock_matrix_repository(self, mocker: MockerFixture, repository: RecommendationsRepository):
        """Фикстура репозитория для тестирования"""

        async def repository_returner():
            yield repository
        mocker.patch('services.tf_idf.TfIdfMatrix._repository', repository_returner)


    @pytest.mark.asyncio
    async def test_initialize(self):
        """
        Проверить инициализацию матрицы, что ничего не ломается
        """
        await TfIdfMatrix().initialize()
        
        
    @pytest.mark.asyncio
    async def test_initialize(self, repository: RecommendationsRepository, mocker: MockerFixture):
        """
        Проверить, что при инициализации выгружается bag of words
        """
        mocker.patch('services.tf_idf.TfIdfMatrix._repository', repository)
        repository.insert_bow([
            (0, 0, 0)
        ])
        matrix = TfIdfMatrix()
        await matrix.initialize()
        assert len(matrix.get_matrix()) == 1