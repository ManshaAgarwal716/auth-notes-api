from datetime import timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from .models import User
from .dependencies import get_current_user,RollChecker,AccessTokenBearer
from src.db.redis import add_token_to_blocklist,is_token_blocked
from fastapi.responses import JSONResponse
from src.users.schemas import UserCreate,UserModel,UserLogin,EmailModel
from src.mail import create_message,mail

from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session

from .services import UserService

from src.users.utils import (
    create_access_token,
    verify_password
)

from src.users.schemas import (
    UserCreate,
    UserModel,
    UserLogin
)

from .dependencies import (
    RefreshTokenBearer
)

roll=RollChecker(allowed_roles=["admin","user"])

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

user_service = UserService()


@router.post(
    "/signup",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED
)
async def signup(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):

    email = user_data.email

    user_exist = await user_service.user_exists(
        email,
        session
    )

    if user_exist:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    new_user = await user_service.create_user(
        user_data,
        session
    )

    return new_user


@router.post("/login")
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session)
):

    user = await user_service.get_user_by_email(
        user_data.email,
        session
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    valid_password = verify_password(
        user_data.password,
        user.password_hash
    )

    if not valid_password:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        user_data={
            "email": user.email,
            "user_uid": str(user.uid)
        }
    )

    refresh_token = create_access_token(
        user_data={
            "email": user.email,
            "user_uid": str(user.uid)
        },
        refresh=True,
        expiry=timedelta(days=2)
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": user.email,
                "uid": str(user.uid)
            }
        }
    )


@router.get("/refresh-token")
async def refresh_token(
    token_data: dict = Depends(
        RefreshTokenBearer()
    )
):

    new_access_token = create_access_token(
        user_data=token_data["user"]
    )

    return JSONResponse(
        content={
            "access_token": new_access_token
        }
    )
@router.get("/me",response_model=UserModel,dependencies=[Depends(roll)])
def get_current_user(user:User=Depends(get_current_user)):
    return user
@router.get("/logout")
async def logout(token_data:dict=Depends(AccessTokenBearer())):
    jti=token_data.get("jti")
    await add_token_to_blocklist(jti)
    return JSONResponse(
        content={
            "message": "Logged out successfully"
        },status_code=status.HTTP_200_OK
    )
@router.post("/send-email")
async def send_email(emails:EmailModel):
    emails=emails.emails
    html="<h1>Test Email from FastAPI Notes App</h1><p>This is a test email sent from the FastAPI Notes application.</p>"
    message=create_message(subject="Verify Your Email",body=html,recipients=emails)
    await mail.send_message(message)
    return {"message":"Emails sent successfully"}