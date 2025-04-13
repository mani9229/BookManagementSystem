import logging
import logging.config
import os

# Define the log directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define the log configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "ERROR",
            "filename": os.path.join(LOG_DIR, "error.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        },
    },
    "loggers": {
        "app": {  # Logger for your application code
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True
        },
        "uvicorn": {  # Logger for Uvicorn (FastAPI)
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False
        },
        "sqlalchemy": { # Logger for SQLAlchemy
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False
        },
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)

# Example Usage (in main.py or other modules):
# import logging
# from app.logging_config import setup_logging
# setup_logging()
# logger = logging.getLogger("app")
# logger.info("Application started")
