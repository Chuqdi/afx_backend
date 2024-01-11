import logging

from termcolor import colored

from src.config import DEBUG


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "blue",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red",
    }

    def format(self, record):
        log_message = super().format(record)
        return colored(log_message, ColoredFormatter.COLORS.get(record.levelname))


def get_logger(name):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.propagate = False

        logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
        handler = logging.StreamHandler()
        formatter = ColoredFormatter(
            "%(levelname)s [%(filename)s:%(lineno)d]: %(asctime)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger
    else:
        return logger


# Setup root logger
root_logger = logging.getLogger()
if not root_logger.hasHandlers():
    root_logger.setLevel(logging.INFO)
    root_logger.propagate = False
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(levelname)s [%(filename)s:%(lineno)d]: %(asctime)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
