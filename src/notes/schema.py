from pydantic import BaseModel
import uuid
from datetime import datetime
class NoteModel(BaseModel):
    uid:uuid.UUID
    title:str
    content:str
    user_uid:uuid.UUID
    created_at:datetime
    updated_at:datetime
class NoteCreate(BaseModel):
    title:str
    content:str
class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None