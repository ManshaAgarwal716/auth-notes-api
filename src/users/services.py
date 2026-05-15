from sqlmodel.ext.asyncio.session import AsyncSession
from src.users.models import User
from src.users.schemas import UserCreate
from src.users.utils import generate_password_hash
from sqlmodel import select
class UserService:
    async def get_user_by_email(self,email:str,session:AsyncSession):
        result=await session.exec(select(User).where(User.email==email))
        return result.first()
    async def user_exists(self,email:str,session:AsyncSession)->bool:
        user=await self.get_user_by_email(email,session)
        return bool(user)
    async def create_user(user_data:UserCreate,session:AsyncSession):
        user_data_dict=user_data.model_dump()
        new_user=User(**user_data_dict)
        new_user.password_hash=generate_password_hash(user_data.password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    
