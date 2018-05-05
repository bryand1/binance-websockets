import config
import logging
import sys
import time


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(config.logfmt, datefmt=config.datefmt)
    formatter.converter = time.gmtime
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
