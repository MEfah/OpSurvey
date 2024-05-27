from fastapi import APIRouter, Depends
from exceptions import UnauthorizedException
from typing import Annotated
from schemas.email import EmailInfo
from transport.handlers.utils.auth import exctract_user_info
from schemas.auth import AuthInfo
from services.email import EmailService


router = APIRouter()


@router.post(
    '/mail',
    status_code=200
)
async def send_email(
    auth_info: Annotated[AuthInfo, Depends(exctract_user_info)],
    email_info: EmailInfo,
    email_service: EmailService = Depends()
):
    """Эндпойнт для осуществления email рассылок"""
    if not auth_info.authorized:
        raise UnauthorizedException()
    
    await email_service.mass_send_email(email_info)