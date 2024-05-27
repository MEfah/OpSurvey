from fastapi import APIRouter, Depends, Path, Query, Cookie, Body, UploadFile, File, Form, Request
from services.auth import AuthService
from exceptions import NotFoundException, UnauthorizedException, ForbiddenException, UnprocessableEntityException, ConflictException
from typing import Annotated
from services.surveys import SurveysService
from transport.handlers.utils.auth import exctract_user_info
from schemas.auth import AuthInfo
from schemas.enums.sort import SortType
from models.survey import Survey
from services.answers import AnswersService
from schemas.answer import SurveyAnswerCreate, SurveyAnswerResponse
from integrations.rabbit_publisher.publisher import publish_message
import json
import uuid
import aiofiles


router = APIRouter()


@router.get(
    '/surveys/{survey_id}/results/ping',
    status_code=200
)
async def get_ping(
    survey_id: str,
    surveys_service: SurveysService = Depends()
):
    """Для отладки"""
    await publish_message('answers', 'created', {'survey_id': survey_id})
    return await surveys_service.get_survey_info(survey_id)



@router.get(
    '/surveys/{survey_id}/results',
    summary='Получить агрегированные результаты опроса',
    status_code=200
)
async def get_results(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    survey_service: SurveysService = Depends(),
    answer_service: AnswersService = Depends()
):
    """Эндпойнт для получения агрегированных результатов опроса"""
    
    survey = await survey_service.get_survey_info(survey_id)
    if not survey:
        raise NotFoundException()
    
    await survey_service.check_user_has_rights(survey, auth_info, True)
    
    return await answer_service.get_survey_results(survey_id)
    

@router.get(
    '/surveys/{survey_id}/answers',
    summary='Получить список ответов на опрос',
    status_code=200
)
async def get_answers(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    survey_service: SurveysService = Depends(),
    answer_service: AnswersService = Depends()
):
    """Эндпойнт для получения списка ответов на результаты опроса"""
    
    survey = await survey_service.get_survey_info(survey_id)
    if not survey:
        raise NotFoundException()
    
    await survey_service.check_user_has_rights(survey, auth_info)
    
    return await answer_service.get_survey_answers(survey_id, limit, offset)


@router.get(
    '/surveys/{survey_id}/answers/my',
    summary='Получить ответ пользователя на опрос',
    status_code=200
)
async def get_answer(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    survey_service: SurveysService = Depends(),
    answer_service: AnswersService = Depends()
):
    """Эндпойнт для получения ответа пользователя на опрос"""
    
    await survey_service.check_user_has_rights(survey_id, auth_info)
    
    res = await answer_service.get_user_answer(survey_id, auth_info.user_id)
    if not res:
        raise NotFoundException()
    return res


@router.post(
    '/surveys/{survey_id}/answers',
    summary='Добавить ответ на опрос',
    status_code=201
)
async def post_answer(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    answer_info: Annotated[SurveyAnswerCreate, Body()],
    survey_service: SurveysService = Depends(),
    answer_service: AnswersService = Depends()
):
    """Эндпойнт для добавления ответа на опрос"""
    
    survey = await survey_service.get_survey_info(survey_id)
    if not survey:
        raise NotFoundException()
    
    await survey_service.check_user_has_rights(survey, auth_info)
    answer_service.fix_question_answer_types(answer_info, survey)

    res = await answer_service.add_survey_answer(survey_id, auth_info.user_id, answer_info)
    # TODO: переместить в BackgroundTask?
    if res:
        await publish_message('answers', 'created', {'survey_id': survey_id})
    return res
    
    
@router.get(
    '/surveys/{survey_id}/answers/{user_id}',
    summary='Получить ответ пользователя на опрос',
    status_code=200
)
async def get_answer(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    user_id: Annotated[str, Path(min_length=32, max_length=32)],
    survey_service: SurveysService = Depends(),
    answer_service: AnswersService = Depends()
):
    """Эндпойнт для получения ответа пользователя на опрос"""
    
    if auth_info.user_id != user_id:
        raise ForbiddenException()
    
    await survey_service.check_user_has_rights(survey_id, auth_info)
    
    res = await answer_service.get_user_answer(survey_id, user_id)
    if not res:
        raise NotFoundException()
    return res
    
    
@router.put(
    '/surveys/{survey_id}/answers/{user_id}',
    summary='Изменить ответ пользователя на опрос',
    status_code=200
)
async def put_answer(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    user_id: Annotated[str, Path(min_length=32, max_length=32)],
    answer_info: Annotated[SurveyAnswerCreate, Body()],
    answer_service: AnswersService = Depends(),
    survey_service: SurveysService = Depends()
):
    """Эндпойнд для изменения ответа пользователя на опрос"""
        
    if auth_info.user_id != user_id:
        raise ForbiddenException()
    survey = await survey_service.get_survey_info(survey_id)
    
    await survey_service.check_user_has_rights(survey, auth_info)
    answer_service.fix_question_answer_types(answer_info, survey)
    
    res = await answer_service.update_survey_answer(survey_id, user_id, answer_info)
    if not res:
        raise NotFoundException()
    return res


@router.delete(
    '/surveys/{survey_id}/answers/{user_id}',
    summary='Удалить ответ пользователя на опрос',
    status_code=204
)
async def delete_answer(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    user_id: Annotated[str, Path(min_length=32, max_length=32)],
    answer_service: AnswersService = Depends()
):
    """Эндпойнт для удаления ответа на опрос"""
        
    if auth_info.user_id != user_id:
        raise ForbiddenException()
    
    res = await answer_service.delete_survey_answer(survey_id, user_id)
    if not res:
        raise NotFoundException()
    return res