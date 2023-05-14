import logging

from .settings import settings


log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(log_formatter)


def init_logging():
    logging.getLogger("uvicorn.error").setLevel(settings.log_level)
    logging.getLogger("uvicorn.access").setLevel(settings.log_level)
    logging.getLogger("fastapi").setLevel(settings.log_level)
    logging.getLogger("uvicorn.error").addHandler(file_handler)
    logging.getLogger("uvicorn.access").addHandler(file_handler)
    logging.getLogger("fastapi").addHandler(file_handler)
