import asyncio
from integrations.rabbit_consumer.consumer import run_consumer
from services.surveys import SurveysService
from services.answers import AnswersService
from schemas.answer import SurveyAnswerCreate, QuestionAnswer
from schemas.survey import SurveyCreated
from schemas.access import AccessUpdated, AccessUpdatedInfo
import ast
import datetime
import json

# TODO вынести в отдельный контейнер

async def run_consumers():
    """Запустить задачи для получения сообщений RabbitMQ"""
    loop = asyncio.get_event_loop()
    loop.create_task(run_consumer('answers_survey_created', 'surveys', 'survey.created', _process_survey_created))
    loop.create_task(run_consumer('answers_access_updated', 'access', 'access', _process_survey_updated))
    


async def _process_survey_created(message: str):
    surveys_service = SurveysService()
    try:
        parsed = SurveyCreated.model_validate_json(message)
        await surveys_service.add_survey_info(parsed)
    except Exception as e:
        # TODO: обработать ошибку
        print(e)
    
    
async def _process_survey_updated(message: str):
    surveys_service = SurveysService()
    try:
        parsed = AccessUpdatedInfo.model_validate_json(message)
        await surveys_service.update_survey_access(parsed.id, parsed.access_updated)
    except Exception as e:
        # TODO: обработать ошибку
        print(e)