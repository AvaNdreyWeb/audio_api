from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    token = Column(UUID(as_uuid=True))
    username = Column(String)


class AudioFile(Base):
    __tablename__ = "audiofiles"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    filename = Column(String)
