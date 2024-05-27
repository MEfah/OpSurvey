import time
from fastapi import APIRouter, Depends, Response, Header, Cookie

from schemas.auth import SignUpInfo, SignInInfo, AuthResponse, RefreshResponse
from schemas.users import UserResponse

from services.users import UsersService
from services.auth import AuthService
from models.user import User
from exceptions import UnprocessableEntityException, ForbiddenException, UnauthorizedException, NotFoundException, ConflictException
from transport.handlers.utils.auth import token_bearer, exctract_user_id
from typing import Annotated
import re
from datetime import datetime, timedelta, timezone
from settings import settings


router = APIRouter()


def generate_and_set_tokens(response: Response, payload: dict, auth_service: AuthService) -> [str, str]:
    access, refresh = auth_service.generate_tokens(payload)
    response.headers["authorization"] = f'Bearer {access}'
    response.set_cookie('refresh-token', refresh, httponly=True, expires=datetime.now(timezone.utc) + timedelta(days=settings.jwt.refresh_ttl_days))
    return [access, refresh]


def set_cookie_id(response: Response, cookie_id: str):
    response.set_cookie('user_id', cookie_id, path='/', expires=datetime.now(timezone.utc) + timedelta(days=settings.cookie_id_ttl_days), httponly=True)


@router.post(
    "/signup", 
    summary="Создать аккаунт",
    response_model=AuthResponse,
    status_code=201)
async def signup(
    response: Response,
    sign_up_info: SignUpInfo,
    cookie_id: Annotated[str | None, Cookie(alias='user_id')] = None,
    auth_service: AuthService = Depends(), 
    users_service: UsersService = Depends()
    ):
    """Эндпойнт для создания аккаунта

    Args:
        response (Response): Ответ
        cookie_id (Annotated[str | None, Cookie(alias='user_id')]): Идентификатор пользователя из куки
        sign_up_info (SignUpInfo): Информация для создания аккаунта
        auth_service (AuthService): Сервис для авторизации и аутентификации
        users_service (UsersService): Сервис для работы с пользователями
    """
    user = await users_service.get_user_by_email(sign_up_info.email)
    if user:
        raise ConflictException("email", "Email занят")
    
    user = await users_service.get_user_by_name(sign_up_info.name)
    if user:
        raise ConflictException("name", "Имя пользователя занято")
    
    pwd_hash = auth_service.hash_password(sign_up_info.password)
    
    # Берем куки-ид, чтобы после создания оставались все пройденные опросы
    if not cookie_id:
        cookie_id = users_service.generate_user_id()
        set_cookie_id(response, cookie_id)
    
    user = await users_service.create_user(cookie_id, sign_up_info.name, sign_up_info.email, pwd_hash)
    
    access_token, refresh_token = generate_and_set_tokens(response, {'user_id': user.id}, auth_service)
    # Генерируем новый идентификатор, чтобы после выхода из аккаунта начиналась новая сессия
    cookie_id = users_service.generate_user_id()
    set_cookie_id(response, cookie_id)
    
    return AuthResponse(user=UserResponse(**user.model_dump()), access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/signin", 
    summary="Войти в аккаунт",
    response_model=AuthResponse,
    status_code=200)
async def signin(response: Response, sign_in_info: SignInInfo, auth_service: AuthService = Depends(), users_service: UsersService = Depends()):
    """Эндпойнт для входа в аккаунт

    Args:
        response (Response): Ответ
        sign_in_info (SignInInfo): Информация для входа в аккаунт
        auth_service (AuthService): Сервис для авторизации и аутентификации
        users_service (UsersService): Сервис для работы с пользователями
    """
    
    user = await users_service.get_user_by_email(sign_in_info.email)
    if not user:
        raise NotFoundException("Пользователь не найден")
    
    if not auth_service.verify_password(sign_in_info.password, user.password):
        raise UnauthorizedException("Указан некорректный пароль")
    
    access_token, refresh_token = generate_and_set_tokens(response, {'user_id': user.id}, auth_service)
    
    return AuthResponse(user=UserResponse(**user.model_dump()), access_token=access_token, refresh_token=refresh_token)
    
    
@router.post(
    "/signout", 
    summary="Выйти из аккаунта",
    status_code=200)
async def signout(response: Response):
    """Эндпойнт для выхода из аккаунта

    Args:
        response (Response): Ответ
    """
    del response.headers["Authorization"]
    response.delete_cookie('refresh-token')
    
    
@router.get(
    "/validate", 
    summary="Проверить, что пользователь авторизован",
    status_code=204)
async def validate(token: Annotated[str | None, Depends(token_bearer)], auth_service: AuthService = Depends()):
    """Эндпойнт для проверки авторизации пользователя

    Args:
        token (Annotated[str  |  None, Depends): jwt-access токен
        auth_service (AuthService, optional): Сервис авторизации

    Raises:
        UnauthorizedException: Токена нет, он не валиден или истек срок жизни
    """
    if not token:
        raise UnauthorizedException()
    
    payload = auth_service.extract_access_payload(token)
    if not payload:
        raise UnauthorizedException()
    
    # return 204 by default
    
    
@router.get(
    "/refresh", 
    summary="Обновить токены доступа",
    response_model=RefreshResponse,
    status_code=200)
async def refresh(response: Response, refresh_token: Annotated[str | None, Cookie(alias='refresh-token')], auth_service: AuthService = Depends()):
    """Эндпойнт для обновления токенов доступа

    Args:
        response (Response): Ответ
        refresh_token (Annotated[str  |  None, Cookie, optional): refresh-токен из куки
        auth_service (AuthService, optional): Сервис авторизации

    Raises:
        UnauthorizedException: refresh-токена нет, он не валиден или истек срок жизни
    """
    if not refresh_token:
        raise UnauthorizedException()
    
    payload = auth_service.extract_refresh_payload(refresh_token)
    if not payload:
        raise UnauthorizedException()
    
    access_token, refresh_token = generate_and_set_tokens(response, payload, auth_service)
    
    return RefreshResponse(access_token=access_token, refresh_token=refresh_token)
    
    
@router.get(
    "/cookieid", 
    summary="Сохранить, сгенерировать или обновить идентификатор пользователя в куки",
    status_code=200)
async def cookieid(response: Response, cookie_id: Annotated[str | None, Cookie(alias='user_id')] = None, users_service: UsersService = Depends()):
    """Эндпойнт для сохрания, генерации или обновления идентификатора пользователя в куки

    Args:
        auth_service (AuthService): Сервис для авторизации и аутентификации
    """
    
    if not cookie_id:
        cookie_id = users_service.generate_user_id()
    
    set_cookie_id(response, cookie_id)
    
    
@router.delete(
    "/cookieid", 
    summary="Удалить куки ид (для отладки)",
    status_code=200)
async def cookieid(response: Response):
    """Эндпойнт для удаления куки ид

    Args:
        auth_service (AuthService): Сервис для авторизации и аутентификации
    """
    response.delete_cookie('user_id')