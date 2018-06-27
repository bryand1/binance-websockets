from app import config
import datetime
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


def json_converter(obj):
    """json.dumps(obj) will fail if obj is not serializable"""
    if isinstance(obj, datetime.datetime):
        return obj.__str__()
