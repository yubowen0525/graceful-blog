from sqlalchemy.sql.coercions import OrderByImpl
from src.schemas.user_schema import UserCreate, UserOut
from typing import List, Optional

from fastapi import APIRouter, Depends

from src.services.user import UserDAL
from src.schemas.user_schema import UserCreate
from src.models.user_model import User
from src.utils.dependencies.database import get_user_dal

router = APIRouter(tags=['user'])


@router.post("/users")
async def create_book(user: UserCreate, user_dal: UserDAL = Depends(get_user_dal)):
    return await user_dal.create_user(user=user)

@router.put("/users/{user_name}")
async def update_book(user_name: str, user: UserCreate,
                      user_dal: UserDAL = Depends(get_user_dal)):
    return await user_dal.update_user(name=user_name, user=user)


@router.get("/users", response_model=List[UserOut])
async def get_all_books(user_dal: UserDAL = Depends(get_user_dal)) -> List[User]:
    result =  await user_dal.get_all_users()
    return result