import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from app.db import User, get_user_db

SECRET = "Iub%i$56ua4bi$u6UI4HIS6U#$6%4^$5646$%^3"

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None) -> None:
        print(f'User {user.id} successfully registered!')
        return await super().on_after_register(user, request)
    

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None)c:
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        return await super().on_after_forgot_password(user, token, request)
    
    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None) -> None:
        print(f'Verification requested for user {user.id}. Verification token: {token}')
        return await super().on_after_request_verify(user, token, request)
    

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    # injection of user db into UserManager class
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')

def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy)

fastapi_Users = FastAPIUsers[User, uuid.UUID](get_user_manager, auth_backends=[auth_backend])
# gets current active user using JWT token
current_active_user = fastapi_Users.current_user(active=True)