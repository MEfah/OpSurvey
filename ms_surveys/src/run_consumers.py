import asyncio
from integrations.rabbit_consumer.consumer import run_consumer
from services.surveys import SurveysService
import ast
import datetime
import json


async def run_consumers():
    """Запустить задачи для получения сообщений RabbitMQ"""
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(run_consumer('surveys_answer_created', 'answers', 'created', _process_result_created), loop=loop)
    asyncio.ensure_future(run_consumer('surveys_user_updated', 'users', 'updated', _process_user_updated), loop=loop)


async def _process_result_created(message: str):
    surveys_service = SurveysService()
    try:
        parsed = json.loads(message)
        await surveys_service.increment_completions_count(parsed['survey_id'])
    except:
        # TODO: Убрать обработку ошибок
        pass
    
    
async def _process_user_updated(message: str):
    surveys_service = SurveysService()

    try:
        parsed = json.loads(message)
        await surveys_service.update_user_info(parsed['id'], parsed['name'], parsed['img_src'])
    except:
        # TODO: Убрать обработку ошибок
        pass