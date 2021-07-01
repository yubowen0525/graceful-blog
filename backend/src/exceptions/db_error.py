from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

async def db_error_handler(_: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse({"errors": str(exc)}, status_code=500)