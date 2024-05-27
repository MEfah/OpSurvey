from typing import Optional

from fastapi import Depends
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session
from settings import settings
from repositories.users_repository import UsersRepository
from schemas.auth import SignUpInfo
from schemas.users import UserUpdate
from models.user import User
from exceptions import UnprocessableEntityException
import uuid


users: list[User] = []


class UsersService():
    """
    Сервис для работы с пользователями
    """
    
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.users_repository = UsersRepository(session)
    
    
    def generate_user_id(self) -> str:
        """
        Генерирует идентификатор пользователя
        """
        return uuid.uuid4().hex
        
    
    async def get_all_users(self) -> list[User]:
        return await self.users_repository.get_all_users()
    
    
    async def get_user_by_id(self, user_id: str) -> User | None:
        """Найти пользователя по идентификатору

        Args:
            user_id (str): идентификатор пользователя

        Returns:
            User | None: модель пользователя
        """
        return await self.users_repository.find_user_by_id(user_id)
    
    
    async def get_user_by_name(self, name: str) -> User | None:
        """Найти пользователя по имени

        Args:
            name (str): имя пользователя

        Returns:
            User | None: имя пользователя
        """
        user = await self.users_repository.find_user_by_name(name)
        return user
    
    
    async def get_user_by_email(self, email: str) -> User | None:
        """Найти пользователя по email

        Args:
            email (str): email по которому находится пользователь

        Returns:
            User | None: имя пользователя
        """
        return await self.users_repository.find_user_by_email(email)
    
    
    async def update_user(self, user_id: str, update_info: UserUpdate) -> User:
        data = update_info.model_dump(exclude_unset=True)
        return await self.users_repository.update_user(user_id, data)
    
    
    async def create_user(self, id: str, name: str, email: str, password: str) -> User | None:
        return await self.users_repository.create_user(id, name, email, password)