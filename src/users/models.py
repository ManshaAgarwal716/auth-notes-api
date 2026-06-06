from sqlmodel import SQLModel, Field,Column,Relationship
from typing import Optional
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
class User(SQLModel,table=True):
    __tablename__="users"   
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, sa_column=Column(pg.UUID(as_uuid=True), primary_key=True))
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    role:str=Field(sa_column=Column(pg.VARCHAR,nullable=False,server_default="user"))
    firstname:str
    lastname:str
    password_hash:str=Field(exclude=True)
    is_verified:bool=Field(default=False)
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    notes: list["Note"] = Relationship(back_populates="user")
    def __repr__(self)->str:
        return f"<User {self.username}>"
