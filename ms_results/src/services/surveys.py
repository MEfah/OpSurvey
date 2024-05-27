from bson import ObjectId

from integrations.db.session import get_collection
from models.survey import Survey
from models.enums.access import AccessSurveyType, AccessResultsType
from schemas.enums.filter import FilterParameterType
from schemas.enums.sort import SortType
from schemas.auth import AuthInfo
from schemas.access import AccessUpdated
from schemas.survey import SurveyCreated
from datetime import datetime, timezone
from exceptions import UnauthorizedException, ForbiddenException
import pymongo


class SurveysService():
    """
    Сервис для работы с опросами
    """
    
    def __init__(self):
        self.collection = get_collection('surveys')
        
    
    async def add_survey_info(self, survey_info: SurveyCreated) -> None:
        """Добавить информацию об опросе"""
        questions_types = [q.question_type for q in survey_info.questions]
        
        survey_dump = Survey(**survey_info.model_dump(), question_types=questions_types).model_dump(by_alias=True)
        survey_dump['_id'] = ObjectId(survey_dump['_id'])
        try:
            await self.collection.insert_one(survey_dump)
        except Exception as e:
            # TODO обработать ошибку
            print(e)
    
    
    async def update_survey_access(self, survey_id: str, access_update: AccessUpdated) -> None:
        """Изменить права доступа к опросу"""
        access_dump = access_update.model_dump(exclude_none=True)
        await self.collection.find_one_and_update(
            {'_id': ObjectId(survey_id)},
            {'$set': access_dump}
        )
    
    
    async def check_user_has_rights(self, survey_id: str, user_info: AuthInfo, results: bool = False) -> None:
        """Проверить наличие прав у пользователя на просмотр результатов опроса"""
        await self.check_user_has_rights(await self.get_survey_info(survey_id), user_info)
        
    
    async def check_user_has_rights(self, survey: Survey, user_info: AuthInfo, results: bool = False) -> None:
        """Проверить наличие прав у пользователя на просмотр результатов опроса"""
    
    
    async def get_survey_info(self, survey_id: str) -> Survey | None:
        """Получить информацию об опросе"""
        res = await self.collection.find_one({'_id': ObjectId(survey_id)})
        return Survey(**res) if res else None
    
    
    async def get_creator_id(self, survey_id: str) -> str | None:
        res = await self.collection.find_one({'_id': ObjectId(survey_id)}, {'creator_id': 1})
        return res['creator_id'] if res else None