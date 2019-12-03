import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .xdg import get_xdg_trading_bot_root, get_logfile_path, initialize_dir, get_logfile_dir

LOG_MAX_MB = 10
LOG_BACKUP_COUNT = 10

class BaseLogFormatter(logging.Formatter):

    def __init__(self, fmt: str, datefmt: str) -> None:
        super().__init__(fmt, datefmt)

    def format(self, record: logging.LogRecord) -> str:
        record.shortname = record.name.split('.')[-1]  # type: ignore
        return super().format(record)


def setup_logger(filename_path: Path, log_level = logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(log_level)
    stream_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(str(filename_path),
                                  maxBytes=1000000 * LOG_MAX_MB,
                                  backupCount=LOG_BACKUP_COUNT)


    formatter = BaseLogFormatter(
        # fmt='%(levelname)8s  %(asctime)s  %(shortname)20s  %(message)s',
        fmt='%(levelname)8s  %(asctime)s  %(name)20s  %(message)s',
        datefmt='%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.addHandler(stream_handler)


def initialize_logger_and_directories(trading_bot_name: str = "trading_bot") -> None:
    base_location = get_xdg_trading_bot_root(trading_bot_name)

    logger_dir = get_logfile_dir(base_location)
    initialize_dir(logger_dir)

    logger_location = get_logfile_path(base_location)

    setup_logger(logger_location)


class BaseLoggingService():
    _logger = None

    @property
    def logger(self):
        if self._logger is None:
            self._logger = logging.getLogger(self.__module__ + '.' + self.__class__.__name__)
        return self._logger