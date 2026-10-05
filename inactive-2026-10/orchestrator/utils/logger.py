import logging
import os
import sys
from datetime import datetime

def setup_logger(name, log_dir="logs"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-5s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        fh = logging.FileHandler(
            os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log"),
            encoding="utf-8"
        )
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
