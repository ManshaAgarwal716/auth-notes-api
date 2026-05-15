from fastapi import APIRouter, Depends,HTTPException,status,Depends
from src.config import set
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .services import UserService
from src.users.models import User
from src.users.utils import generate_password_hash,verify_password
from src.users.schemas import UserCreate,UserModel,UserLogin
router=APIRouter(prefix="/users",tags=["Users"])
user_service=UserService()
@router.post("/signup",
             response_model=UserModel,
             status_code=status.HTTP_201_CREATED)
async def signup(user_data:UserCreate,session:AsyncSession=Depends(get_session)): 
    email=user_data.email
    user_exist=await user_service.user_exists(email,session)

    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this email already exists")   
    new_user=await user_service.create_user(user_data,session)
    return new_user
@router.post("/login")
async def login(user_data:UserLogin,session:AsyncSession=Depends(get_session)):
    user=await user_service.get_user_by_email(user_data.email,session)
    password=user_data.password
    hashed_password=generate_password_hash(password)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not verify_password(password,hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid credentials")
    return user

