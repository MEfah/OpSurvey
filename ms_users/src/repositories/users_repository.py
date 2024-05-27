from typing import Any, Dict, Optional, Type, Union

from pydantic.main import BaseModel
from sqlalchemy import Column, insert, update
from sqlalchemy.engine import CursorResult, Result, Row
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select
from sqlmodel.sql.expression import SelectOfScalar
from models.user import User
import uuid


class UsersRepository():
    """
    Репозиторий для пользователей
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализация репозитория
        """

        self.session = session
        
        
    async def get_all_users(self) -> list[User]:
        cursor = await self.session.execute(select(User))
        return cursor.scalars().all()
        
        
    async def find_user_by_id(self, user_id: str) -> User | None:
        cursor = await self.session.execute(select(User).where(User.id == user_id))
        return cursor.scalar()
        
        
    async def find_user_by_name(self, name: str) -> User | None:
        cursor = await self.session.execute(select(User).where(User.name == name))
        return cursor.scalar()
        
        
    async def find_user_by_email(self, email: str) -> User | None:
        cursor = await self.session.execute(select(User).where(User.email == email))
        return cursor.scalar()
    
    
    async def update_user(self, user_id: str, data: dict):
        if not data:
            raise ValueError('no update args passed')
        
        statement = (
            update(User)
            .where(User.id == user_id)
            .values(data).returning(User)
        )

        cursor = await self.session.execute(statement)
        user = cursor.fetchone()
        await self.session.commit()
        return user[0] if user else None
        
        
    async def create_user(self, id: str, name: str, email: str, password: str) -> User | None:
        statement = insert(User).values(id = id, name=name, email=email, password=password).returning(User)

        cursor = await self.session.execute(statement)
        user = cursor.fetchone()
        await self.session.commit()
        return user[0] if user else None