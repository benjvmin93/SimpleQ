from pydantic import BaseModel


class Circuit(BaseModel):
    name: str
    user_id: int
    class Config:
        orm_mode = True


class User(BaseModel):
    username: str

    class Config:
        orm_mode = True
