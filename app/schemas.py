from pydantic import BaseModel


class User(BaseModel):
    id: int
    token: str
    username: str

    class Config:
        orm_mode = True
