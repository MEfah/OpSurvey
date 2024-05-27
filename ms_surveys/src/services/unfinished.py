import logging.config
from typing import Optional

from bson import ObjectId
from fastapi import Depends
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_collection
from settings import Settings
from exceptions import UnprocessableEntityException
from schemas.survey import SurveyCreate, SurveyInfoList, AccessUpdate, AccessResponse
from schemas.unfinished import UnfinishedCreate, UnfinishedResponse, UnfinishedInfoList
from models.survey import Survey, UnfinishedSurvey
import uuid
from datetime import datetime, timezone


class UnfinishedSurveysService():
    """
    Сервис для работы с опросами
    """
    
    def __init__(self):
        self.collection = get_collection('unfinished')
                
        
    def _replaceId(self, model: dict) -> dict:
        model['id'] = model['_id']
        return model
    
    
    def _replaceIdList(self, models: list[dict]) -> list[dict]:
        for model in models:
            model['id'] = model['_id']
        return models
        
        
    async def get_creator_id(self, unfinished_id: str) -> str | None:
        res = await self.collection.find_one({'_id': unfinished_id}, {'creator_id': 1})
        return res['creator_id'] if res else None
        
        
    async def get_users_unfinished_surveys(self, user_id: str, limit: int, offset: int) -> UnfinishedInfoList:
        return UnfinishedInfoList(surveys=self._replaceIdList(await self.collection.find({'creator_id': user_id}).skip(offset).limit(limit).to_list(limit)))


    async def create_unfinished_survey(self, unfinished_create: UnfinishedCreate) -> UnfinishedResponse | None:
        survey = UnfinishedSurvey(updated_date=datetime.now(timezone.utc), **unfinished_create.model_dump())
        survey_dump = survey.model_dump(by_alias=True, exclude=["id"])
        result = await self.collection.insert_one(
            survey_dump
        )
        
        if result:
            survey_dump['_id'] = result.inserted_id
        
        return UnfinishedResponse(**self._replaceId(survey_dump)) if result else None
    
    
    async def get_unfinished_survey(self, unfinished_id: str) -> UnfinishedResponse | None:
        survey = await self.collection.find_one({'_id': ObjectId(unfinished_id)})
        return UnfinishedResponse(**self._replaceId(survey)) if survey else None
    
    
    async def update_unfinished_survey(self, unfinished_id: str, unfinished_create: UnfinishedCreate) -> UnfinishedResponse | None:
        result = await self.collection.find_one_and_update(
            {'_id': ObjectId(unfinished_id)},
            {'$set': unfinished_create.model_dump(by_alias=True, exclude_none=True)},
            return_document=True
        )
        return UnfinishedResponse(**self._replaceId(result)) if result else None
    
    
    async def delete_unfinished_survey(self, unfinished_id: str) -> bool:
        delete_result = await self.collection.delete_one({"_id": ObjectId(unfinished_id)})
        
        if delete_result.deleted_count == 1:
            return True
        
        return False
    