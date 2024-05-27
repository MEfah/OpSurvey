from fastapi import APIRouter, Depends, Path, Query, Cookie, Body, UploadFile, File, Form
from schemas.survey import SurveyCreate, SurveyInfoList
from services.auth import AuthService
from services.files import FilesService
from exceptions import NotFoundException, UnauthorizedException, ForbiddenException, UnprocessableEntityException, ConflictException
from typing import Annotated
from transport.handlers.utils.auth import token_bearer
from services.surveys import SurveysService, AccessUpdate
from services.unfinished import UnfinishedSurveysService
from schemas.unfinished import UnfinishedCreate
from transport.handlers.utils.auth import exctract_user_info
from schemas.auth import AuthInfo
import json

router = APIRouter()


@router.post(
    '/',
    summary='Сохранить незавершенный опрос',
    status_code=201
)
async def post_unfinished(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    unfinished_create: Annotated[str, Form()],
    file: Annotated[UploadFile | None, File()] = None,
    unfinished_surveys_service: UnfinishedSurveysService = Depends(),
    files_service: FilesService = Depends()
):
    """"""
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    create_survey = UnfinishedCreate(**json.loads(unfinished_create))
    create_survey.creator_id = auth_info.user_id
    
    if file:
        saved_path = await files_service.save_file(file)
        if saved_path:
            create_survey.img_src = saved_path
    else:
        create_survey.img_src = None
    
    return await unfinished_surveys_service.create_unfinished_survey(create_survey)


@router.get(
    '/{unfinished_id}',
    summary='Получить незаконченный опрос',
    status_code=200
)
async def get_unfinished(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    unfinished_id: Annotated[str, Path()],
    unfinished_surveys_service: UnfinishedSurveysService = Depends()
):
    """"""
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    survey = await unfinished_surveys_service.get_unfinished_survey(unfinished_id)

    if survey.creator_id != auth_info.user_id:
        raise ForbiddenException()
    
    return survey


@router.put(
    '/{unfinished_id}',
    summary='Обновить незаконченный опрос',
    status_code=200
)
async def post_unfinished(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    unfinished_id: Annotated[str, Path()],
    unfinished_create: Annotated[str, Form()],
    file: Annotated[UploadFile | None, File()] = None,
    unfinished_surveys_service: UnfinishedSurveysService = Depends(),
    files_service: FilesService = Depends()
):
    """"""
    print('asdfasdfasdfasdf')
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    survey = await unfinished_surveys_service.get_unfinished_survey(unfinished_id)
    
    if not survey:
        raise NotFoundException()
    
    if survey.creator_id != auth_info.user_id:
        raise ForbiddenException()

    create_survey = UnfinishedCreate(**json.loads(unfinished_create))
    create_survey.creator_id = survey.creator_id
    
    if file:
        saved_path = await files_service.save_file(file)
        if saved_path:
            create_survey.img_src = saved_path
    else:
        create_survey.img_src = survey.img_src
    
    res = await unfinished_surveys_service.update_unfinished_survey(unfinished_id, create_survey)

    if res and file and survey.img_src:
        files_service.remove_file(survey.img_src)

    return res


@router.delete(
    '/{unfinished_id}',
    summary='Удалить незаконченный опрос',
    status_code=204
)
async def delete_unfinished(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    unfinished_id: Annotated[str, Path()],
    with_picture: Annotated[bool, Query()],
    unfinished_surveys_service: UnfinishedSurveysService = Depends(),
    files_service: FilesService = Depends()
):
    """"""
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    survey = await unfinished_surveys_service.get_unfinished_survey(unfinished_id)
    
    if not survey:
        raise NotFoundException()
    
    if survey.creator_id != auth_info.user_id:
        raise ForbiddenException()
    
    res = await unfinished_surveys_service.delete_unfinished_survey(unfinished_id)
    if res and with_picture and survey.img_src:
        files_service.remove_file(survey.img_src)