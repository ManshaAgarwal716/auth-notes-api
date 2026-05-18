from .models import Note
from .schema import NoteCreate, NoteUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select 

class NoteService:
    async def create_note(self, note_data: NoteCreate, user_id: int, session: AsyncSession) -> Note:
        new_note_dict=note_data.model_dump()
        new_note=Note(**new_note_dict,user_id=user_id)
        session.add(new_note)
        await session.commit()
        await session.refresh(new_note)
        return new_note
    async def get_user_notes(self,user_id:int,session:AsyncSession):
        statement=select(Note).where(Note.user_id==user_id)
        result=await session.exec(statement)
        return result.all()
    async def get_note(self,note_uid: str, session: AsyncSession):
       statement = select(Note).where(
            Note.uid == note_uid
        )
       result = await session.exec(statement)
       note = result.first()
       return note
    async def delete_note(self,note:Note,session:AsyncSession):
        note_to_delete=await self.get_note(note.uid, session)
        if not note_to_delete:
            return None

        await session.delete(note_to_delete)
        await session.commit()
        return True
    async def update_note(self,note_uid:str,update_data:NoteUpdate,session:AsyncSession):
            update_note=await self.get_note(note_uid,session)
            if not update_note:
                return None
            update_note_dict=update_data.model_dump()
            for k,v in update_note_dict.items():
                setattr(update_note,k,v)
            await session.commit()
            await session.refresh(update_note)
            return update_note