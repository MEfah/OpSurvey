from fastapi import APIRouter, Depends, Path, Query, Cookie, Body
from schemas.survey import SurveyCreate, SurveyInfoList
from services.auth import AuthService
from exceptions import NotFoundException, UnauthorizedException, ForbiddenException, UnprocessableEntityException, ConflictException
from typing import Annotated
from transport.handlers.utils.auth import exctract_user_info
from schemas.auth import AuthInfo
from services.surveys import SurveysService, AccessUpdate
from services.unfinished import UnfinishedSurveysService

router = APIRouter()


@router.get(
    '/{user_id}/surveys',
    summary="Получить опросы пользователя",
    status_code=200
)
async def get_users_surveys(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    user_id: Annotated[str, Path()],
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    surveys_service: SurveysService = Depends()
):
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    if auth_info.user_id != user_id:
        raise ForbiddenException()
    
    return await surveys_service.get_users_surveys(user_id, limit, offset)


@router.get(
    '/{user_id}/surveys/unfinished',
    summary='Получить незавершенные опросы пользователя',
    status_code=200
)
async def post_survey(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    user_id: Annotated[str, Path()],
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    unfinished_surveys_service: UnfinishedSurveysService = Depends()
):
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    if auth_info.user_id != user_id:
        raise ForbiddenException()
    
    return await unfinished_surveys_service.get_users_unfinished_surveys(user_id, limit, offset)
