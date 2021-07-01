
from src.extension import async_session
from src.services.user import UserDAL


async def get_user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)