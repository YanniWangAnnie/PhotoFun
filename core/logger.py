import logging
from enum import Enum

logging.basicConfig(filename="pf.log", level=logging.ERROR, format='%(levelname)s: %(asctime)s %(message)s')


def log(message,Log_level):
    if Log_level == LogLevel.error:
        logging.error(message)
    elif Log_level == LogLevel.warning:
        logging.warning(message)
    else:
        logging.info(message)
    

class LogLevel(Enum):
    info = 0
    warning = 1
    error = 2

    