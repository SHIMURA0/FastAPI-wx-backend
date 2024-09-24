# app/services/users.py

from typing import Optional, Self
from fastapi import Depends
from app.models.WeChat.user import User as UserModel
from app.schemas.WeChat.user import UserInfo as UserSchema
from app.crud.WeChat.user import UserRepository, get_user_repository
from typing import Annotated


class UserService:
    def __init__(
            self,
            user_repository: UserRepository
    ) -> None:
        self.user_repository = user_repository

    @classmethod
    async def create(
            cls,
            user_repository: UserRepository
    ) -> Self:
        return cls(user_repository)

    async def get_user_info(
            self,
            user_open_id: str
    ) -> Optional[UserSchema]:
        db_user = await self.user_repository.get_by_openid(user_open_id)
        if not db_user:
            return None

        return UserSchema(
            real_name=db_user.real_name,
            openid=db_user.openid,
        )

    async def create_user(
            self,
            user_data: UserSchema
    ) -> UserModel:
        db_user: UserModel = await self.user_repository.create(user_data)
        return db_user

    async def update_user(
            self,
            user_openid: str,
            user_real_name: str
    ) -> None:
        await self.user_repository.update_name(user_openid, user_real_name)


    async def delete_user(
            self,
            user_id: int
    ) -> bool:
        """
        删除用户。

        参数:
        - user_id: int, 用户ID

        返回:
        - bool: 删除成功返回 True，否则返回 False
        """
        return await self.user_repository.delete(user_id)


async def get_user_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    """
    Dependency function to obtain an instance of UserService.

    This asynchronous function serves as a dependency injector for FastAPI routes
    that require UserService functionality. It encapsulates the creation process
    of UserService, ensuring that each request receives a fresh instance with an
    appropriate database session.

    Args:
        db (AsyncSession): An asynchronous database session.
            This is automatically injected by FastAPI's dependency system.
            The session is obtained from the get_db_dependency,
            which manages the lifecycle of the database connection.

    Returns:
        UserService: A newly created instance of the UserService class.
            This instance is initialized with the provided database session
            and is ready to perform user-related operations.

    Raises:
        Any exceptions that might occur during the creation of UserService,
        such as database connection issues or initialization errors.

    Usage:
        In FastAPI route definitions:
        @app.get("/users")
        async def get_users(user_service: UserService = Depends(get_user_service)):
            return await user_service.get_all_users()

    Note:
        - This function is asynchronous and should be used with FastAPI's
          dependency injection system.
        - It ensures that each request gets a new UserService instance,
          promoting request isolation and proper resource management.
        - The database session is automatically managed by FastAPI,
          including closing the session after the request is completed.
        - This approach allows for easier testing and mocking of UserService
          in unit tests by overriding this dependency.
          :param user_repository:
    """
    return await UserService.create(user_repository)
