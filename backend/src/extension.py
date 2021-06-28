from loguru import logger

logging = logger.bind(
    hostName=gethostname(),
)
