from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schema import NoteModel,NoteCreate,NoteUpdate
from .models import Note
from src.users.models import User
from .services import NoteService
from src.users.dependencies import get_current_user,RollChecker,AccessTokenBearer
note_service=NoteService()
note=APIRouter(tags=["Notes"])
@note.get("/notes", response_model=list[NoteModel])
async def get_notes(current_user: User = Depends(get_current_user),session:AsyncSession=Depends(get_session)):
    notes=await note_service.get_user_notes(current_user.uid,session)
    return notes
@note.post("/notes",response_model=NoteModel,status_code=status.HTTP_201_CREATED)
async def create_note(note_data:NoteCreate,current_user: User = Depends(get_current_user),session:AsyncSession=Depends(get_session)):
    new_note=await note_service.create_note(note_data,current_user.uid,session)
    return new_note
@note.get("/notes/{note_id}", response_model=NoteModel)
async def get_a_note(note_id:str,current_user: User = Depends(get_current_user),session:AsyncSession=Depends(get_session)):
    note=await note_service.get_note(note_id,session)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    if note.user_uid != current_user.uid:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return note
@note.patch("/notes/{note_id}",response_model=NoteModel)
async def update_a_note(note_id:str,update_data:NoteUpdate,current_user: User = Depends(get_current_user),session:AsyncSession=Depends(get_session)):
    existing_note=await note_service.get_note(note_id,session)
    if not existing_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    if existing_note.user_uid != current_user.uid:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    update_a_note=await note_service.update_note(note_id,update_data,session)   
    return update_a_note
@note.delete("/notes/{note_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_note(note_id:str,current_user: User = Depends(get_current_user),session:AsyncSession=Depends(get_session)):
    existing_note=await note_service.get_note(note_id,session)
    if not existing_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    if existing_note.user_uid != current_user.uid:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    await note_service.delete_note(existing_note,session)
    return

