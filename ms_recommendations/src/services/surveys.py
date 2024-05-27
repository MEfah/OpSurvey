from integrations.db.session import get_session
from models.survey import Survey
from schemas.access import AccessUpdated
from schemas.survey import SurveyCreated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from integrations.db.session import get_session
from repositories.recommendations import RecommendationsRepository


class SurveysService():
    """
    Сервис для работы с опросами
    """
    
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.repository = RecommendationsRepository(session)
        
    
    async def add_survey_info(self, survey_info: SurveyCreated) -> int:
        """Добавить информацию об опросе

        Args:
            survey_info (SurveyCreated): создаваемый опрос

        Returns:
            int: идентификатор опроса как текстового документа
        """
        return await self.repository.add_survey(Survey(**survey_info.model_dump(), access_type=0))
    
    
    async def update_survey_access(self, survey_id: str, access_update: AccessUpdated) -> None:
        """Изменить права доступа к опросу"""
        await self.repository.update_survey_access(survey_id=survey_id, new_access=access_update.access_survey.access_type_survey)

        
    
    async def add_completion(self, user_id: str, survey_id: str) -> None:
        """Добавить запись о прохождении опроса"""
        await self.repository.add_completion(user_id, survey_id)