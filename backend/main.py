from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.exceptions.http_error import http_error_handler
from src.exceptions.validation_error import http422_error_handler
from src.api.routes.api import router as api_router
from src.configs.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from src.core.events import create_start_app_handler, create_stop_app_handler
from src.extension import logger
import traceback
import uuid
import json
import sys

def create_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=API_PREFIX)

    return application


def register_logging(app):
    def customized_serializer(message):
        """Customized the fields we need."""
        record = message.record

        fields = {
            "level": record["level"].name,
            "message": dict(detail=record["message"]),
            "timestamp": record["time"].isoformat(),
            "traceId": record["extra"].get("traceId", str(uuid.uuid4())),
            "taskId": record["extra"].get("taskId", str(uuid.uuid4())),
            "type": "trace",
            "serviceName": "szn",
            "componentName": "Controller SASEOne Proxy",
        }

        if "traceId" in record["extra"]:
            del record["extra"]["traceId"]

        if "taskId" in record["extra"]:
            del record["extra"]["taskId"]

        if record["exception"]:
            fields["message"]["exception"] = "".join(
                traceback.format_exception(
                    type(record["exception"].value),
                    record["exception"].value,
                    record["exception"].traceback,
                )
            )
        # Gather the bidning fields
        fields["message"].update(record["extra"])
        fileds = json.dumps(fields)
        print(fileds, file=sys.stdout)

    logger.remove(handler_id=None)
    # logger.add(sys.stderr, level=app.config["LOG_LEVEL"])
    logger.add(customized_serializer, level=app.config["LOG_LEVEL"])






app = create_application()
    