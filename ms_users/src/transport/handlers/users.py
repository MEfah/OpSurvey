from fastapi import APIRouter, Depends, Path, Query, File, UploadFile, Form
from schemas.auth import SignUpInfo
from schemas.users import UserUpdate, UserResponse
from services.users import UsersService
from services.auth import AuthService
from exceptions import NotFoundException, UnauthorizedException, ForbiddenException, UnprocessableEntityException, ConflictException
from typing import Annotated, Optional
from transport.handlers.utils.auth import token_bearer
from integrations.rabbit_publisher.publisher import publish_message
from models.user import User
import aiofiles
import pathlib
import uuid
import json

router = APIRouter()


@router.get(
    "/checkemail", 
    summary="Проверить email",
    status_code=200)
async def checkEmail(email: Annotated[str | None, Query()] = None, users_service: UsersService = Depends()):
    user = await users_service.get_user_by_email(email)
    if user:
        raise ConflictException("email", "Email занят")


@router.get(
    "/checkname", 
    summary="Проверить имя",
    status_code=200)
async def checkEmail(name: str, users_service: UsersService = Depends()):
    user = await users_service.get_user_by_name(name)
    if user:
        raise ConflictException("name", "Имя пользователя занято")


@router.get(
    '/all',
    summary="Получить всех пользователей",
    response_model=list[User],
    status_code=200
)
async def get_all_users(users_service: UsersService = Depends()):
    users = await users_service.get_all_users()
    return users


@router.get(
    '/allprotected',
    summary="Получить всех пользователей с проверкой авторизации",
    response_model=list[User],
    status_code=200
)
async def get_all_users_protected(token: Annotated[str | None, Depends(token_bearer)], 
                                  users_service: UsersService = Depends(),
                                  auth_service: AuthService = Depends()):
    if not token:
        raise UnauthorizedException()
    
    payload = auth_service.extract_access_payload(token)
    if not payload:
        raise UnauthorizedException()
    
    users = await users_service.get_all_users()
    return users


@router.get(
    "/find", 
    summary="Получить пользователя по имени",
    response_model=UserResponse,
    status_code=200)
async def get_user_by_name(name: Annotated[str | None, Query(min_length=5, max_length=70)] = None, users_service: UsersService = Depends()):
    """Эндпойнт для получения пользователя по имени

    Args:
        id (str): Имя пользователя
        users_service (UsersService): Сервис для работы с пользователями
    """
    if name is None:
        raise UnprocessableEntityException('Не указано ни одного параметра поиска')
    
    user = await users_service.get_user_by_name(name)
    
    if not user:
        raise NotFoundException("Пользователь не найден")
    return UserResponse(**user.model_dump())


@router.get(
    "/{user_id}", 
    summary="Получить пользователя по идентификатору",
    response_model=UserResponse,
    status_code=200)
async def get_user_by_id(user_id: str = Path(min_length=32, max_length=32), users_service: UsersService = Depends()):
    """Эндпойнт для получения пользователя по идентификатору

    Args:
        id (str): Идентификатор пользователя
        users_service (UsersService): Сервис для работы с пользователями
    """
    user = await users_service.get_user_by_id(user_id)
    if not user:
        raise NotFoundException("Пользователь не найден")
    return UserResponse(**user.model_dump())


@router.patch(
    "/{user_id}", 
    summary="Обновить информацию о пользователе",
    response_model=UserResponse,
    status_code=200)
async def update_user(user_id: Annotated[str, Path(min_length=32, max_length=32)], 
                      token: Annotated[str | None, Depends(token_bearer)],
                      file: Annotated[UploadFile | None, File()] = None, 
                      update_user_info: Annotated[str | None, Form()] = None, 
                      users_service: UsersService = Depends(), 
                      auth_service: AuthService = Depends()):
    """Эндпойнт для обновления информации о пользователе

    Args:
        token (Annotated[str  |  None, Depends): access-токен
        update_user_info (UserUpdate): Данные для обновления пользователя
        user_id (Annotated[str, Path, optional): Идентификатор обновляемого пользователя
        users_service (UsersService, optional): Сервис пользователей
        auth_service (AuthService, optional): Сервис авторизации.

    Raises:
        UnauthorizedException: Отсутствует access-токен или он не валиден
        ForbiddenException: Нет прав (один пользователь обновляет информацию о одругом пользователе)
        ConflictException: Имя уже используется

    Returns:
        UserResponse: Ответ с информацией о пользователе
    """
    if not file and not update_user_info:
        raise UnprocessableEntityException('Не указана информация для обновления пользователя')
    
    if not token:
        raise UnauthorizedException()
    
    payload = auth_service.extract_access_payload(token)
    if not payload:
        raise UnauthorizedException()
    
    if not user_id == payload['user_id']:
        raise ForbiddenException()
    
    
    try: # Если не указано данных
        if update_user_info:
            update_user_info = UserUpdate(**(json.loads(update_user_info)))
        else:
            update_user_info = UserUpdate()
    except:
        update_user_info = UserUpdate()
    
    if update_user_info and update_user_info.name:
        name_user = await users_service.get_user_by_name(update_user_info.name)
        if name_user:
            raise ConflictException('name', 'Пользователь с указанным именем уже существует')
    
    if file:
        user = await users_service.get_user_by_id(user_id)
        
        file_name = uuid.uuid4().hex + '.' + file.filename.split('.')[-1]
        file_path = '/media/users/' + file_name
        
        async with aiofiles.open(file_path, 'wb') as file_to:
            content = await file.read()
            await file_to.write(content)
            update_user_info.img_src = file_path
            if user.img_src and user.img_src != '':
                path = pathlib.Path(user.img_src)
                if path.exists():
                    path.unlink()

    user = await users_service.update_user(user_id, update_user_info)
    response = UserResponse(**user.model_dump())
    print('got response')
    if user:
        print('publishing')
        await publish_message('users', 'updated', response.model_dump_json())
    return response