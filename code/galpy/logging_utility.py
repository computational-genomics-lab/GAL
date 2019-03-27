import logging
from pathlib import Path, PurePath


def logger_function(name, filename):
    filename = PurePath(filename)
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(name)s: %(message)s')
        try:
            file_handler = logging.FileHandler(filename)
        except (TypeError, AttributeError) as e:
            filename = str(filename)
            file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        logger.addHandler(stream_handler)
    return logger


class GalLogging:
    def __init__(self, name, filename):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s:%(name)s: %(message)s')

            file_handler = logging.FileHandler(filename)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
