from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class DownloadLink(BaseModel):
    link: str


class User(BaseUser):
    id: int
    token: str

    class Config:
        orm_mode = True
