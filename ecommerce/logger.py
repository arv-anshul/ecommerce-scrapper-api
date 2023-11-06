import logging
from datetime import datetime as dt
from pathlib import Path

logger_instances = {}


def __configure_logger(logger: logging.Logger, fp: Path):
    logger.setLevel(logging.DEBUG)

    fp.parent.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(fp)
    formatter = logging.Formatter(
        "[%(asctime)s]:%(levelname)s:%(name)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_logger(logger_name: str) -> logging.Logger:
    # Check if the logger instance already exists
    if logger_name in logger_instances:
        return logger_instances[logger_name]

    run_id = dt.now().strftime("%d%m%y-%H%M")
    log_file_path = Path(f"logs/{run_id}.log")

    logger = logging.getLogger(logger_name)
    __configure_logger(logger, log_file_path)
    logger_instances[logger_name] = logger

    return logger
