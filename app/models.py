import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from config import db_url

Base = declarative_base()

engine = create_async_engine(db_url)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Note(Base):
    __tablename__ = "notes"

    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    isChecked = sa.Column(sa.Boolean, nullable=False)


class NoteModel(BaseModel):
    id: int
    content: str
    isChecked: bool
