from fastapi import FastAPI, Depends, UploadFile, Body, status, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from . import schemas, crud, database
from typing import Annotated

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def download_audio(id: str, user: int, db: Session = Depends(get_db)):
    filename = crud.get_audiofile_by_id(db, id)
    if not filename:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    audio_path = f'/audio/{user}/{filename}'
    return FileResponse(audio_path, media_type='audio/mp3', filename=filename)


@app.post("/user", response_model=schemas.User, response_model_exclude={"username"})
async def create_user(username: Annotated[str, Body()], db: Session = Depends(get_db)):
    db_user = crud.create_user(db, username)
    return schemas.User(
        id=db_user.id,
        token=str(db_user.token),
        username=db_user.username
    )


@app.post("/upload")
async def upload_audio(user_id: Annotated[int, Body()], token: Annotated[str, Body()], file: UploadFile, db: Session = Depends(get_db)):
    filename = await crud.save_audiofile(user_id, file)
    if not filename:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"[{file.filename[:-4]}] already exist")
    audio_id = crud.create_audiofile(db, filename)
    return {"download_link": f'http://127.0.0.1:8000/?id={audio_id}&user={user_id}'}
