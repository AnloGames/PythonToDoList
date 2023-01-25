import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from os import path, curdir

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app import config

Base = declarative_base()

eng_path = path.abspath(curdir)
eng_path = eng_path[0:-3]
print(eng_path)
engine = create_async_engine(f"sqlite+aiosqlite:///{eng_path}ToDo.db")

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

