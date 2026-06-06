from pydantic import BaseModel, EmailStr, Field
from typing import List
import uuid
from datetime import datetime
from src.notes.schema import NoteModel
class UserModel(BaseModel):
    uid:uuid.UUID
    username:str
    email:str
    firstname:str
    lastname:str
    password_hash:str=Field(exclude=True)
    is_verified:bool
    created_at:datetime
    updated_at:datetime
class UserNote(UserModel):
    notes:list[NoteModel]
class UserCreate(BaseModel):
    username:str=Field(max_length=8)
    email:str=Field(max_length=40)
    password:str=Field(min_length=6)
class UserLogin(BaseModel):
    email:str=Field(max_length=40)
    password:str=Field(min_length=6)
class EmailModel(BaseModel):
    emails:List[str]