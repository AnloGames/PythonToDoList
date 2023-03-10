from fastapi import APIRouter, Depends, HTTPException, Body, Response
from app.dependencies import get_session
from app.models import Note, NoteModel
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy


router = APIRouter()
@router.get("/items")
async def get_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(sqlalchemy.select(Note))
    notes = result.scalars().all()
    if not notes:
        raise HTTPException(status_code=404, detail="NONE")
    response_data = []
    for note in notes:
        response_data.append({'id': note.id, 'content': note.content, 'isChecked': note.isChecked})
    return response_data


@router.post("/items/create")
async def create_item(content: str = Body(..., embed=True), session: AsyncSession = Depends(get_session)):
    note = Note(content=content, isChecked=False)
    session.add(note)
    await session.commit()
    return {'id': note.id, 'content': note.content, 'isChecked': note.isChecked}


@router.post("/items/delete")
async def delete_item(id: int = Body(..., embed=True), session: AsyncSession = Depends(get_session)):
    result = await session.execute(sqlalchemy.select(Note).filter(
        Note.id == id
    ))
    note = result.scalars().first()
    await session.delete(note)
    await session.commit()
    return Response(None, 204)


@router.post("/items/update")
async def update_item(note: NoteModel = Body(...), session: AsyncSession = Depends(get_session)):
    result = await session.execute(sqlalchemy.select(Note).filter(
        Note.id == note.id
    ))
    db_note = result.scalars().first()
    if not db_note:
        raise HTTPException(status_code=404, detail="NONE")
    await session.execute(sqlalchemy.update(Note).filter(
        Note.id == note.id
    ).values({'content': note.content, 'isChecked': note.isChecked}))
    await session.commit()
    return {'id': note.id, 'content': note.content, 'isChecked': note.isChecked}




