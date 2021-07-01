from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    password: str
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True
