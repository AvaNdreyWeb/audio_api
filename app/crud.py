from sqlalchemy.orm import Session
from fastapi import UploadFile

from . import models
import uuid

import os
import pydub

AUDIO_ROOT = os.path.abspath("/audio")


def create_user(db: Session, username: str):
    new_user = models.User(token=uuid.uuid4(), username=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def save_audiofile(user_id: int, file: UploadFile):
    user_dir = os.path.abspath(f'{AUDIO_ROOT}/{user_id}')
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)

    tmp_path = os.path.abspath(f'{user_dir}/{file.filename}')
    if os.path.exists(tmp_path):
        return ''

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
    audio = db.query(models.AudioFile).filter(models.AudioFile.id == uuid.UUID(id)).first()
    if audio:
        return audio.filename
    return ''
