import os
from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import crud, database, schemas

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def download_audio(id: str, user: int, db: Session = Depends(get_db)):
    filename = crud.get_audiofile_by_id(db, id)
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid file id."
        )
    valid_path = f"/audio/{user}/{filename}"
    if not os.path.exists(valid_path):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid user id."
        )
    return FileResponse(valid_path, media_type="audio/mp3", filename=filename)


@app.post(
        "/user",
        response_model=schemas.User,
        response_model_exclude={"username"}
)
async def create_user(user: schemas.BaseUser, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user.username)
    return schemas.User(
        id=db_user.id,
        token=str(db_user.token),
        username=db_user.username
    )


@app.post("/upload", response_model=schemas.DownloadLink)
async def upload_audio(
    user_id: Annotated[int, Body()],
    token: Annotated[str, Body()],
    file: UploadFile,
    db: Session = Depends(get_db)
):
    code = crud.check_user_token(db, user_id, token)
    if code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )
    if code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Invalid user id."
        )
    if file.content_type[-3:] != "wav":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid file type. Service provide only .wav extension."
        )
    filename = await crud.save_audiofile(user_id, file)
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Given filename is occupied."
        )
    audio_id = crud.create_audiofile(db, filename)
    return schemas.DownloadLink(
        link=f"http://127.0.0.1:8000/?id={audio_id}&user={user_id}"
    )
