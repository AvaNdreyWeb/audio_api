import os
import uuid

import pydub
from fastapi import UploadFile, status
from sqlalchemy.orm import Session

from . import models

AUDIO_ROOT = "/audio"


def create_user(db: Session, username: str):
    new_user = models.User(token=uuid.uuid4(), username=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def save_audiofile(user_id: int, file: UploadFile):
    user_dir = f"{AUDIO_ROOT}/{user_id}"
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)

    tmp_path = f"{user_dir}/{file.filename}"
    if os.path.exists(tmp_path[:-4]+".mp3"):
        return ""

    tmp = open(tmp_path, "wb")
    tmp.write(await file.read())
    tmp.close()

    new_path = f"{tmp_path[:-4]}.mp3"
    sound = pydub.AudioSegment.from_wav(tmp_path)
    sound.export(new_path, format="mp3")
    os.remove(tmp_path)
    return f"{file.filename[:-4]}.mp3"


def create_audiofile(db: Session, filename: str):
    new_audiofile = models.AudioFile(id=uuid.uuid4(), filename=filename)
    db.add(new_audiofile)
    db.commit()
    db.refresh(new_audiofile)
    return str(new_audiofile.id)


def get_audiofile_by_id(db: Session, id: str):
    audio = db.query(models.AudioFile).filter(
        models.AudioFile.id == uuid.UUID(id)
    ).first()
    if audio:
        return audio.filename
    return ""


def check_user_token(db: Session, user_id: int, token: str):
    db_user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    if not db_user:
        return status.HTTP_404_NOT_FOUND
    if db_user.token != uuid.UUID(token):
        return status.HTTP_401_UNAUTHORIZED
    return status.HTTP_200_OK
