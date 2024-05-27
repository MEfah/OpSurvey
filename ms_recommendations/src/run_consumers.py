import asyncio
from integrations.rabbit_consumer.consumer import run_consumer
from services.surveys import SurveysService
from services.recommendations import RecommendationsService
from integrations.db.session import get_session
from schemas.survey import SurveyCreated
from schemas.access import AccessUpdatedInfo
import ast
import datetime
import json


async def run_consumers():
    """Запустить задачи для получения сообщений RabbitMQ"""
    loop = asyncio.get_event_loop()
    loop.create_task(run_consumer('recommendations_answer_created', 'answers', 'created', _process_result_created))
    loop.create_task(run_consumer('recommendations_survey_created', 'surveys', 'survey.created', _process_survey_created))
    loop.create_task(run_consumer('recommendations_access_updated', 'access', 'access', _process_survey_updated))


async def _process_result_created(message: str):
    surveys_service = SurveysService(await get_session())
    try:
        parsed = json.loads(message)
        await surveys_service.add_completion(parsed['user_id'], parsed['survey_id'])
    except:
        # TODO: Убрать обработку ошибок
        pass

    
async def _process_survey_created(message: str):
    surveys_service = SurveysService(await get_session())
    recommendations_service = RecommendationsService(await get_session())
    try:
        parsed = SurveyCreated.model_validate_json(message)
        doc_id = await surveys_service.add_survey_info(parsed)
        await recommendations_service.add_survey_bow(doc_id, parsed)
    except Exception as e:
        # TODO: Убрать обработку ошибок
        print(e)
    
    
async def _process_survey_updated(message: str):
    surveys_service = SurveysService(await get_session())
    try:
        parsed = AccessUpdatedInfo.model_validate_json(message)
        await surveys_service.update_survey_access(parsed.id, parsed.access_updated)
    except Exception as e:
        # TODO: Убрать обработку ошибок
        print(e)