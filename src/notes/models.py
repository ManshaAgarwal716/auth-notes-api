from sqlmodel import Field, SQLModel,Column,Field
from sqlalchemy.dialects import postgresql as pg
import uuid
from datetime import datetime

class Note(SQLModel,table=True):
    __tablename__="notes"
    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,sa_column=Column(pg.UUID(as_uuid=True),primary_key=True)
    )
    title:str
    content:str
    user_uid: uuid.UUID = Field(
        foreign_key="users.uid"
    )
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))