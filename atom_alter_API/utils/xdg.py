import os

from pathlib import Path

from typing import Union

LOG_DIRNAME = 'logs'
LOG_FILENAME = 'trading_bot.log'

def get_home() -> Path:
    try:
        return Path(os.environ['HOME'])
    except KeyError:
        raise Exception('$HOME environment variable not set')


def get_xdg_data_home() -> Path:
    try:
        return Path(os.environ['XDG_DATA_HOME'])
    except KeyError:
        return get_home() / '.local' / 'share'


def get_xdg_trading_bot_root(trading_bot_name: str = 'trading_bot') -> Path:
    """
    Returns the base directory under which trading bot will store all data.
    """
    try:
        return Path(os.environ['XDG_TRADING_BOT_ROOT'])
    except KeyError:
        return get_xdg_data_home() / trading_bot_name

def get_logfile_dir(data_dir: Path) -> Path:
    """
    Return the path to the log file.
    """
    return data_dir / LOG_DIRNAME

def get_logfile_path(data_dir: Path) -> Path:
    """
    Return the path to the log file.
    """
    return get_logfile_dir(data_dir) / LOG_FILENAME

def is_under_path(base_path: Union[str, Path], path: Union[str, Path]) -> bool:
    base_path = Path(base_path).resolve()
    path = Path(path).resolve()
    if base_path == path:
        return False
    return str(path).startswith(str(base_path))


def initialize_dir(directory_path: Path) -> None:
    should_create_dir = not directory_path.exists()

    if should_create_dir:
        directory_path.mkdir(parents=True, exist_ok=True)

