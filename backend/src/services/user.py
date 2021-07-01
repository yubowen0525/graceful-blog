from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from src.schemas.user_schema import UserCreate
from src.models.user_model import User

class UserDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, user:UserCreate):
        new_book = User(name=user.name, email=user.email, password=user.password)
        self.db_session.add(new_book)
        await self.db_session.flush()

    async def get_all_users(self) -> List[User]:
        q = await self.db_session.execute(select(User).order_by(User.id))
        return q.scalars().all()

    async def update_user(self, *, name: Optional[str] = "bowen", user: UserCreate):
        q = update(User).where(User.name == name)
        if user.name:
            q = q.values(name=name)
        if user.email:
            q = q.values(email=user.email)
        if user.password:
            q = q.values(password=user.password)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)