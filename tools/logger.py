import logging
import os
from tools import config


def get_logger():
    logger = logging.getLogger("default")
    return logger


def setup_logger():
    logger = logging.getLogger("default")
    logger.setLevel(logging.DEBUG)
    custom_format = logging.Formatter('%(asctime)s : %(message)s')

    # Create handlers
    log_folder = config.output
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    f_handler = logging.FileHandler(log_folder + '/log.txt', 'a', 'utf-8')
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    f_handler.setFormatter(custom_format)

    # Add handlers to the logger
    logger.addHandler(f_handler)

    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.DEBUG)
    c_handler.setFormatter(custom_format)
    logger.addHandler(c_handler)