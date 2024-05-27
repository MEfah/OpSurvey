from fastapi import APIRouter, Depends, Path, Query, Cookie, Body, UploadFile, File, Form, Request
from services.auth import AuthService
from services.recommendations import RecommendationsService
from services.surveys import SurveysService
from typing import Annotated
from transport.handlers.utils.auth import exctract_user_info
from schemas.auth import AuthInfo
from exceptions import ForbiddenException
import httpx


router = APIRouter()


@router.get(
    '/'
)
async def get_recommendations(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    surveys_service: SurveysService = Depends(),
    recommendations_service: RecommendationsService = Depends()
):
    ids = await recommendations_service.get_recommended_surveys()
    ids_param = ','.join(ids)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://ms_surveys:8888/api/v1/surveys/pick?surveys={ids_param}')

        if response.status_code == 200:
            return {"data": response.json()}
        else:
            raise ForbiddenException()