from datetime import datetime
from typing import List

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.filters import LimitOffset
from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.params import Parameter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.exceptions import NotFoundException

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User


async def provide_users_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session=db_session)


class UserController(Controller):
    path = "/users"
    tags = ["Users"]
    dependencies = {"repo": Provide(provide_users_repo)}

    @get()
    async def list_users(
        self, db_session: AsyncSession, offset: int = 0, limit: int = 100
    ) -> List[UserResponse]:
        query = select(User).offset(offset).limit(limit)
        result = await db_session.execute(query)
        users = result.scalars().all()
        
        return [
            UserResponse.model_validate(user)
            for user in users
        ]

    @post()
    async def create_user(self, db_session: AsyncSession, data: UserCreate) -> UserResponse:
        user = User(
            name=data.name,
            surname=data.surname,
            password=data.password,  #Я бы хешировал, но в задании не сказано)
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        return UserResponse.model_validate(user)

    @get("/{user_id:int}")
    async def get_user(
        self, db_session: AsyncSession, user_id: int = Parameter(title="User ID")
    ) -> UserResponse:
        query = select(User).where(User.id == user_id)
        result = await db_session.execute(query)
        user = result.scalar_one_or_none()
        
        if user is None:
            raise NotFoundException(f"{user_id} не найден")
            
        return UserResponse.model_validate(user)

    @put("/{user_id:int}")
    async def update_user(
        self,
        db_session: AsyncSession,
        data: UserUpdate,
        user_id: int = Parameter(title="User ID"),
    ) -> UserResponse:
        query = select(User).where(User.id == user_id)
        result = await db_session.execute(query)
        user = result.scalar_one_or_none()
        
        if user is None:
            raise NotFoundException(f"{user_id} не найден")
            
        update_data = data.model_dump(exclude_unset=True)
        
        if update_data:
            for key, value in update_data.items():
                setattr(user, key, value)
            await db_session.commit()
            await db_session.refresh(user)

        return UserResponse.model_validate(user)

    @delete("/{user_id:int}")
    async def delete_user(
        self, db_session: AsyncSession, user_id: int = Parameter(title="User ID")
    ) -> None:
        query = select(User).where(User.id == user_id)
        result = await db_session.execute(query)
        user = result.scalar_one_or_none()
        
        if user is None:
            raise NotFoundException(f"{user_id} не найден")
            
        await db_session.delete(user)
        await db_session.commit() 