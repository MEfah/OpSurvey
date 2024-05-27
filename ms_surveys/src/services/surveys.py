from bson import ObjectId

from integrations.db.session import get_collection
from schemas.survey import SurveyCreate, SurveyResponse, SurveyInfoList, AccessUpdate, AccessResponse
from models.survey import Survey
from models.enums.access import AccessSurveyType, AccessResultsType
from schemas.filter import FilterParam, FilterRange
from schemas.enums.filter import FilterParameterType
from schemas.enums.sort import SortType
from schemas.auth import AuthInfo
from datetime import datetime, timezone
from exceptions import UnauthorizedException, ForbiddenException
import pymongo


class SurveysService():
    """
    Сервис для работы с опросами
    """
    
    def __init__(self):
        self.collection = get_collection('surveys')
        
        
    async def get_creator_id(self, survey_id: str) -> str | None:
        res = await self.collection.find_one({'_id': ObjectId(survey_id)}, {'creator_id': 1})
        return res['creator_id'] if res else None
        
        
    async def get_all_surveys(self, limit: int, offset: int):
        # TODO: Возвращать только нужные поля
        return await self.collection.find().skip(offset).limit(limit).to_list(limit)
    
    
    def _build_filter_range(self, filter_range: FilterRange) -> dict:
        query = {}
        if filter_range.range_from:
            query['$gte'] = filter_range.range_from
        if filter_range.range_to:
            query['$lte'] = filter_range.range_to
        return query
    
    
    def _build_filter_query(self, query: dict, filter_params: list[FilterParam]):
        param_map = {
            FilterParameterType.COMPLETIONS: 'completion_count',
            FilterParameterType.COMPLETION_TIME: 'completion_time',
            FilterParameterType.CREATION_DATE: 'creation_date',
            FilterParameterType.QUESTIONS: 'question_count',
            FilterParameterType.REQUIRED_QUESTIONS: 'required_count'
        }
        
        for param in filter_params:
            if param.parameter_type == FilterParameterType.RESULTS_ACCESSIBLE:
                query['access_results.access_type_results'] = AccessResultsType.ALL
            else:
                query[param_map[param.parameter_type]] = self._build_filter_range(param.value)
    
    
    def _build_sort_query(self, sort_param: SortType, sort_ascending: bool) -> list:
        param_map = {
            SortType.COMPLETIONS: 'completion_count',
            SortType.COMPLETION_TIME: 'completion_time',
            SortType.CREATION_DATE: 'creation_date',
            SortType.QUESTIONS: 'question_count',
            SortType.REQUIRED_QUESTIONS: 'required_count',
            SortType.POPULARITY: 'completion_count'
        }
        
        return [(param_map[sort_param], pymongo.ASCENDING if sort_ascending else pymongo.DESCENDING)]
    
    
    def _replaceId(self, model: dict) -> dict:
        model['id'] = model['_id']
        return model
    
    
    def _replaceIdList(self, models: list[dict]) -> list[dict]:
        for model in models:
            model['id'] = model['_id']
        return models
    
    
    async def get_surveys(self,
                          limit: int,
                          offset: int,
                          authorized: bool = False,
                          search_text: str | None = None,
                          filter_params: list[FilterParam] | None = None,
                          sorting_param: SortType | None = None,
                          sort_ascending: bool = False) -> SurveyInfoList:
        
        access_types = [AccessSurveyType.ALL]
        if authorized:
            access_types = [AccessSurveyType.ALL, AccessSurveyType.ONLY_AUTHORIZED]
            
        query = { 'access_survey.access_type_survey': {'$in': access_types} }
            
        if search_text:
            query['$text'] = {
                '$search': search_text
            }
            
        if filter_params:
            self._build_filter_query(query, filter_params)
        
        # Получить только те поля, которые есть в модели + переименовать id
        cursor = self.collection.find(query)
        if sorting_param:
            cursor = cursor.sort(self._build_sort_query(sorting_param, sort_ascending))
        
        
        # TODO: Возвращать только нужные поля
        return SurveyInfoList(surveys=self._replaceIdList(await cursor.skip(offset).limit(limit).to_list(limit)))
    
    
    async def get_surveys_from_list(self, survey_ids: list[str]):
        """Вернуть информацию об опросах в списке"""
        obj_ids = [ObjectId(id) for id in survey_ids]
        return SurveyInfoList(surveys=self.collection.find({'_id': {'$in': obj_ids}}).to_list(len(survey_ids)))
    
    
    def _check_user_has_rigts_for_survey(self, survey: Survey, user_info: AuthInfo, password: str | None) -> bool:
        """
        Определить, есть ли у пользователя права на просмотр опроса
        """
        if survey.creator_id == user_info.user_id:
            return True
        
        access_type = survey.access_survey.access_type_survey;

        if access_type in [AccessSurveyType.ONLY_AUTHORIZED, AccessSurveyType.ONLY_LIST, AccessSurveyType.ONLY_LIST_AND_KEYS] and not user_info.authorized:
            raise UnauthorizedException('Только авторизованные пользователи могут просматривать этот опрос')
        
        if access_type == AccessSurveyType.NONE:
            raise ForbiddenException('Нет прав на просмотр опроса')

        if access_type == AccessSurveyType.ONLY_LIST and user_info.user_id not in survey.access_survey.access_list:
            raise ForbiddenException('Нет прав на просмотр опроса')

        if access_type == AccessSurveyType.ONLY_KEYS and password not in survey.access_survey.access_keys:
            raise ForbiddenException('Нет прав на просмотр опроса')
        
        if access_type == AccessSurveyType.ONLY_LIST_AND_KEYS \
            and user_info.user_id not in survey.access_survey.access_list \
            and password not in survey.access_survey.access_keys:
            raise ForbiddenException('Нет прав на просмотр опроса')
        
        return True
    
    
    async def get_survey_for_user(self, id: str, user_info: AuthInfo, password: str | None) -> SurveyResponse:
        """
        Получить опрос для пользователя, либо вернуть ошибку Forbidden/Unauthorized
        """
        survey = await self.collection.find_one(
            {"_id": ObjectId(id)}
        )
        
        # Проверить, есть ли права, если нет, то выбросить ошибку
        if survey:
            self._check_user_has_rigts_for_survey(Survey(**survey), user_info, password)
        
        return SurveyResponse(**self._replaceId(survey)) if survey else None
    
    
    async def get_survey(self, id: str) -> SurveyResponse:
        """
        Получить опрос по идентификатору
        """
        survey = await self.collection.find_one(
            {"_id": ObjectId(id)}
        )
        return SurveyResponse(**self._replaceId(survey)) if survey else None
    
    
    async def create_survey(self, survey_create: SurveyCreate) -> SurveyResponse:
        """
        Создать опрос
        """
        
        total_text_len = len(survey_create.name) + (len(survey_create.description) if survey_create.description else 0)
        for q in survey_create.questions:
            total_text_len += len(q.name) + (len(survey_create.description) if survey_create.description else 0)
        
        survey = Survey(
            creation_date=datetime.now(timezone.utc), 
            completion_time=max(1, round(total_text_len/860)),
            question_count=len(survey_create.questions), 
            required_count=len(list(filter(lambda x: x.required == True, survey_create.questions))),
            **survey_create.model_dump())
        
        survey_dump = survey.model_dump(by_alias=True, exclude=["id"])
        result = await self.collection.insert_one(
            survey_dump
        )
        
        if result:
            survey_dump['_id'] = result.inserted_id
        
        return SurveyResponse(**self._replaceId(survey_dump)) if result else None
    
    
    async def delete_survey(self, id: str) -> bool:
        """Удалить опрос

        Args:
            id (str): идентификатор опроса

        Returns:
            bool: True, если опрос был удален
        """
        
        delete_result = await self.collection.delete_one({"_id": ObjectId(id)})
        
        if delete_result.deleted_count == 1:
            return True
        
        return False
    
    
    async def get_survey_access(self, id: str) -> AccessResponse:
        """
        Получить настройки доступа опроса по идентификатору
        """
        survey = await self.collection.find_one(
            {"_id": ObjectId(id)}, {'access_survey': 1, 'access_results':1, 'access_api': 1}
        )
        return AccessResponse(**survey) if survey else None
    
    
    async def update_survey_access(self, id: str, access_update: AccessUpdate) -> AccessResponse:
        """Изменить настройки доступа опроса

        Args:
            id (str): идентификатор опроса
            update_access (UpdateAccess): новые настройки доступа
        """
        
        result = await self.collection.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': access_update.model_dump(exclude_none=True)},
            return_document=True,
        )
        return AccessResponse(**result) if result else None
    
    
    async def get_users_surveys(self, user_id: str, limit: int, offset: int) -> SurveyInfoList:
        return SurveyInfoList(surveys=self._replaceIdList(await self.collection.find({'creator_id': user_id}).skip(offset).limit(limit).to_list(limit)))
    
    
    async def increment_completions_count(self, survey_id: str):
        await self.collection.find_one_and_update({'_id': ObjectId(survey_id)}, {'$inc': {'completion_count': 1}})
        
        
    async def update_user_info(self, user_id: str, user_name: str | None, img_src: str | None):
        set_query = dict()
        if user_name:
            set_query['creator_name'] = user_name
        if img_src:
            set_query['creator_img_src'] = img_src
        await self.collection.update_many(
            {'creator_id': user_id}, 
            {'$set': set_query}
        )