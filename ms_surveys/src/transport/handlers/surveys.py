from fastapi import APIRouter, Depends, Path, Query, Cookie, Body, UploadFile, File, Form, Request
from schemas.survey import SurveyCreate, SurveyInfoList
from services.auth import AuthService
from exceptions import NotFoundException, UnauthorizedException, ForbiddenException, UnprocessableEntityException, ConflictException
from typing import Annotated
from transport.handlers.utils.query import get_filter_params
from services.surveys import SurveysService, AccessUpdate
from services.files import FilesService
from transport.handlers.utils.auth import exctract_user_info
from schemas.auth import AuthInfo
from schemas.filter import FilterParam, FilterParamList
from schemas.enums.sort import SortType
from models.survey import Survey
from schemas.search import SearchParams
from integrations.rabbit_publisher.publisher import publish_message
import json
import uuid
import aiofiles


router = APIRouter()


@router.get(
    '/',
    summary="Получить опросы",
    response_model_by_alias=True,
    status_code=200
)
async def get_surveys(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    filter_param_list: Annotated[FilterParamList | None, Depends(get_filter_params)] = None,
    search_text: Annotated[str | None, Query(alias='searchText')] = None,
    sort_type: Annotated[SortType | None, Query(alias='sortType')] = None,
    sort_ascending: Annotated[bool | None, Query(alias='sortAscending')] = False,
    surveys_service: SurveysService = Depends()
):
    """"""
    filter_params = filter_param_list.filter_params if filter_param_list else None
    return await surveys_service.get_surveys(limit, offset, auth_info.authorized, search_text, filter_params, sort_type, sort_ascending)


@router.post(
    '/',
    summary='Создать опрос',
    status_code=201
)
async def post_survey(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    create_survey: Annotated[str, Form()], 
    file: Annotated[UploadFile | None, File()] = None, 
    surveys_service: SurveysService = Depends(),
    files_service: FilesService = Depends()
):
    """"""
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    create_survey = SurveyCreate(**json.loads(create_survey))
    if not auth_info.user_id == create_survey.creator_id:
        raise ForbiddenException()
    
    if file:
        saved_path = await files_service.save_file(file)
        if saved_path:
            create_survey.img_src = saved_path
    else:
        create_survey.img_src = None
    
    res = await surveys_service.create_survey(create_survey)
    if res:
        await publish_message('surveys', 'survey.created', res.model_dump_json())
    return res


@router.get(
    '/{survey_id}',
    summary='Получить опрос по идентификатору',
    status_code=200
)
async def get_survey(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    password: Annotated[str | None, Query()] = None,
    surveys_service: SurveysService = Depends()
):
    """"""
    survey = await surveys_service.get_survey_for_user(survey_id, auth_info, password)
    
    if not survey:
        raise NotFoundException('Опрос не найден')
    
    return survey


@router.delete(
    '/{survey_id}',
    summary='Удалить опрос',
    status_code=204
)
async def delete_survey(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    surveys_service: SurveysService = Depends()
):
    """"""
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    creator_id = await surveys_service.get_creator_id(survey_id)
    
    if not creator_id:
        raise NotFoundException()
    
    if creator_id != auth_info.user_id:
        raise ForbiddenException()
    
    await surveys_service.delete_survey(survey_id)
    # returns 204 by default
    
    
@router.get(
    '/pick',
    summary="Получить опросы из списка",
    response_model_by_alias=True,
    status_code=200
)
async def get_surveys(
    surveys: str,
    surveys_service: SurveysService = Depends()):
    """
    """
    return surveys_service.get_surveys_from_list(surveys.split(','))
    
    
@router.get(
    '/{survey_id}/access',
    summary='Получить настройки доступа',
    status_code=200
)
async def get_access(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    surveys_service: SurveysService = Depends()
):
    """"""
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    creator_id = await surveys_service.get_creator_id(survey_id)
    
    if not creator_id:
        raise NotFoundException()
    
    if creator_id != auth_info.user_id:
        raise ForbiddenException()
    
    return await surveys_service.get_survey_access(survey_id)


@router.patch(
    '/{survey_id}/access',
    summary='Изменить настройки доступа',
    status_code=200
)
async def patch_access(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    access_update: AccessUpdate,
    survey_id: Annotated[str, Path(min_length=24, max_length=24)],
    surveys_service: SurveysService = Depends()
):
    """"""
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    creator_id = await surveys_service.get_creator_id(survey_id)
    
    if not creator_id:
        raise NotFoundException()
    
    if creator_id != auth_info.user_id:
        raise ForbiddenException()

    res = await surveys_service.update_survey_access(survey_id, access_update)
    if res:
        await publish_message('access', 'access', {'id': survey_id, 'access_updated': res.model_dump()})
    return res