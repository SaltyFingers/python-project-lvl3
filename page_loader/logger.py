import logging

FORMAT = ('|%(levelname)s| %(message)s')


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(FORMAT))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.CRITICAL)
    logger.addHandler(get_stream_handler())
    return logger
