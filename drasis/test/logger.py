import os
import logging


def configure_global_logger():
    level = logging.INFO
    if os.environ.get('TEST_DRASIS_DEBUG', '') == '1':
        level = logging.DEBUG

    logging.basicConfig(
        level=level, format="[%(name)s] - %(levelname)s - %(message)s"
    )


def get_dummy_logger(name):
    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)
    if os.environ.get('TEST_DRASIS_DEBUG', '') == '1':
        logger.setLevel(logging.DEBUG)

    return logger
