import logging
from logging.handlers import RotatingFileHandler


# ----------------------------------------------------------------------
def create_rotating_log(path):
    """
    Creates a rotating log
    """
    # logging

    # logging.basicConfig(force=True)
    format = '%(asctime)s;%(levelname)s;%(message)s'
    logging.basicConfig(format=format)
    formatter = logging.Formatter(format)

    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.DEBUG)

    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=5000,
                                  backupCount=5)
    # set formatter also for the files.
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
