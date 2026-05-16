from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status, Depends
from typing import List
from .models import User

from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session

from .utils import decode_access_token
from .services import UserService


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):

        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request) -> dict:

        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_access_token(token)

        if not self.valid_token(token_data):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        self.verify_token_data(token_data)

        return token_data


    def valid_token(self, token_data: dict) -> bool:

        return True if token_data and "user" in token_data else False


    def verify_token_data(self, token_data: dict):

        raise NotImplementedError(
            "override this with child class"
        )


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict):

        if token_data.get("refresh"):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide access token"
            )

        return True


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict):

        if not token_data.get("refresh"):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide refresh token"
            )

        return True


async def get_current_user(
    token_data: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
):

    user_email = token_data["user"]["email"]

    user_service = UserService()

    user = await user_service.get_user_by_email(
        user_email,
        session
    )
    return user

    return user
class RollChecker:
    def __init__(self,allowed_roles:List[str]):
        self.allowed_roles=allowed_roles
    def __call__(self,user:User=Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource"
            )
        return True
