from fastapi import Depends, Header, Cookie
from typing import Annotated
from services.auth import AuthService
from schemas.auth import AuthInfo
from exceptions import ForbiddenException


def token_bearer(authorization: Annotated[str | None, Header(alias="authorization")] = None) -> str | None:
    """
    Использовать в Depends, чтобы извлечь токен
    """
    if not authorization:
        return None
    
    parts = authorization.split(' ')
    if len(parts) != 2 or parts[0] != 'Bearer':
        return None
    return parts[1]


def exctract_user_info(
    cookie_id: Annotated[str | None, Cookie(alias='user_id')] = None, 
    token: Annotated[str | None, Depends(token_bearer)] = None,
    auth_service: AuthService = Depends()
    ) -> AuthInfo:
    """
    Использовать в Depends, чтобы извлечь идентификатор пользователя.
    Проверяет токен в заголовке Authorization и идентификатор в куки
    """
    
    token_id = None
    
    if token:
        payload = auth_service.extract_access_payload(token)
        if payload:
            token_id = payload['user_id']
    
    if not token_id:
        if not cookie_id:
            raise ForbiddenException()
        
        auth_info = AuthInfo(authorized=False, user_id=cookie_id)
    
    else:
        auth_info = AuthInfo(authorized=True, user_id=token_id)


    return auth_info