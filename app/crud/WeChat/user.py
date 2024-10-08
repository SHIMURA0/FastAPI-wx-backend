# app/crud/user.py
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression

from app.db.session import get_async_db
from app.models.WeChat.user import User
from app.api.dependencies.Wechat.db import get_db_dependency
from app.schemas.WeChat.user import (
    UserInfo,
    NameUpdate
)
from typing import (
    Optional,
    cast,
    Annotated
)


class UserRepository:

    def __init__(
            self,
            db: AsyncSession
    ) -> None:
        self.db: AsyncSession = db

    async def get_by_id(
            self,
            user_id: int
    ) -> Optional[User]:
        """通过用户ID获取用户。"""
        result = await (
            self.db.execute(
                select(User)
                .filter(
                    cast(BinaryExpression, User.id == user_id)
                )
            )
        )
        return result.scalars().first()

    async def get_by_openid(
            self,
            openid: str
    ) -> Optional[User]:
        """通过openid获取用户，类似于get方法。"""
        query = select(User).where(cast(BinaryExpression, User.openid == openid))  # 使用 .where() 代替 .filter() （可选）
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create(
            self,
            user: UserInfo
    ) -> User:
        """创建新用户。接受一个UserCreate Pydantic模型，将其转换为User ORM模型，添加到数据库，提交更改，刷新对象（获取数据库生成的ID），然后返回。"""
        new_id: int = await User.generate_id(self.db)
        db_user: User = User(
            id=new_id,
            real_name=user.real_name,
            openid=user.openid,
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_name(
            self,
            user_openid: str,
            name_to_update: str
    ) -> Optional[User]:

        db_user: Optional[User] = await self.get_by_openid(user_openid)
        if db_user:
            db_user.real_name = name_to_update
            await self.db.commit()
            await self.db.refresh(db_user)
        return db_user

    async def delete(self, user_id: int) -> bool:

        db_user: Optional[User] = await self.get_by_id(user_id)
        if db_user:
            await self.db.delete(db_user)
            await self.db.commit()
            return True
        return False


async def get_user_repository(
        db: Annotated[AsyncSession, Depends(get_async_db)]
) -> UserRepository:
    return UserRepository(db)
