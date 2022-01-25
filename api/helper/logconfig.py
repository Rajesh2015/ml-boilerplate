from pydantic import BaseModel
from os import environ, path
from dotenv import load_dotenv
from pathlib import Path

basedir = path.abspath(path.dirname(__file__))
base_path = Path(__file__).parent
load_dotenv(path.join(basedir, '.env'))


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = environ.get('NAME')
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        environ.get('NAME'): {"handlers": ["default"], "level": LOG_LEVEL},
    }
