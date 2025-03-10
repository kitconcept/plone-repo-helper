__version__ = "1.0.0a0"
import logging


PACKAGE_NAME = "plone_repo_helper"


def _setup_logging():
    logger = logging.getLogger(PACKAGE_NAME)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    return logger


logger = _setup_logging()
