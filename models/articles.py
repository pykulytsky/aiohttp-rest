from typing import Optional
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

from ..config import DB_URI
from datetime import datetime


Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI))
session = scoped_session(Session)
Base = declarative_base()


class Article(Base):

    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(50))
    created = Column(DateTime, default=datetime.now())
    update = Column(DateTime, default=datetime.now())
    created_by = Column(String(50), blank=True)

    def __init__(
        self,
        title: str,
        description: str,
        created_by: Optional[str] = None
    ) -> None:
        self.title = title
        self.description = description
        self.update = datetime.now()
        self.created_by = created_by

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def to_json(self):
        to_serialize = [
            'id', 'title', 'description', 'created', 'update', 'created_by'
        ]

        data = dict()
        for attr in to_serialize:
            data[attr] = getattr(self, attr)

        return data
